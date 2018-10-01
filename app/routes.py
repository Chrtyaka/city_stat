from datetime import datetime
import os
import sys
from flask import request, json, Response, send_file, render_template
from sqlalchemy import and_, text

from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
import pprint
from app import app, db

from .models import Category, Feature, Country, Province, Area, Locality, FeatureLocality


EPSILON = sys.float_info.epsilon

def date_in_base(date):
    if date == "":
        date = datetime.today ( )
    else:
        date = datetime.strptime ( date + ",1,1", "%Y,%m,%d" )
    return date

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))


def rgb_price(value,value_min,value_max):
    colors = [(0, 255, 0), (255, 0, 0)]
    minval, maxval = 0, 1
    value = (value - value_min) / (value_max - value_min)
    r, g, b = convert_to_rgb(minval, maxval, value, colors)
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

@app.route ( '/' )
def index():
    return render_template ( 'index.html' )

engine = db.engine


@app.route ( '/add_category', methods=[ 'POST' ] )
def add_category():
    json_string = request.get_json ( force=True )
    if 'categoryname' in json_string:
        name = Category.query.filter_by ( categoryname=json_string[ 'categoryname' ] ).first ( )
        if name is None:
            category = Category ( categoryname=json_string[ 'categoryname' ] )
            db.session.add ( category )
            db.session.commit ( )
            return "Category created!"
        else:
            return "Category already exists!"
    if 'categorys' in json_string:
        for category in json_string[ 'categorys' ]:
            category_name = Category.query.filter_by ( categoryname=category[ 'categoryname' ] ).first ( )
            if category_name is None:
                cat = Category ( categoryname=category[ 'categoryname' ] )
                db.session.add ( cat )
        db.session.commit ( )
        return "Categorys created!"


@app.route ( '/add_feature', methods=[ 'POST' ] )
def add_feature():
    json_string = request.get_json ( force=True )

    category = Category.query.filter_by ( categoryname=json_string[ 'category_id' ] ).first ( )
    if category is None:
        category = Category ( categoryname=json_string[ 'category_id' ] )
        db.session.add ( category )
        db.session.commit ( )
    if 'featurename' in json_string:
        feature_name = json_string[ 'featurename' ]
        dimension = json.string[ 'dimension' ]
        featureadd = Feature.query.filter (
            and_ ( Feature.featurename.like ( feature_name ), Feature.featurename.like ( dimension ),
                   Feature.category_id.like ( category.id ) ) ).first ( )
        if featureadd is None:
            feature = Feature ( featurename=feature_name, category_id=category.id, dimension=dimension )
            db.session.add ( feature )
            db.session.commit ( )
            return "Feature created!"
        else:
            return "Feature already exists!"

    if 'features' in json_string:
        for feature in json_string[ 'features' ]:
            feature_add = Feature.query.filter ( and_ ( Feature.featurename.like ( feature[ 'featurename' ] ),
                                                        Feature.featurename.like ( feature[ 'dimension' ] ),
                                                        Feature.category_id.like ( category.id ) ) ).first ( )
            if feature_add is None:
                feat = Feature ( featurename=feature[ 'featurename' ], dimension=feature[ 'dimension' ],
                                 category_id=category.id )
                db.session.add ( feat )
        db.session.commit ( )
        return "Features created!"


@app.route ( '/add_country', methods=[ 'POST' ] )
def add_country():
    json_string = request.get_json ( force=True )
    if 'countryname' in json_string:
        country = Country.query.filter_by ( countryname=json_string[ 'countryname' ] ).first ( )
        if country is None:
            country_name = Country ( countryname=json_string[ 'countryname' ],
                                     coordinates=json_string[ 'coordinates' ] )
            db.session.add ( country_name )
            db.session.commit ( )
            return "Country created!"
        else:
            return "Country already exists!"

    if 'countrys' in json_string:
        for coun in json_string[ 'countrys' ]:
            coun_add = Country.query.filter_by ( countryname=coun[ 'countryname' ] ).first ( )
            if coun_add is None:
                c = Country ( countryname=coun[ 'countryname' ], coordinates=coun[ 'coordinates' ] )
                db.session.add ( c )
        db.session.commit ( )
        return "Countrys created!"


@app.route ( '/add_province', methods=[ 'POST' ] )
def add_province():
    json_string = request.get_json ( force=True )
    country = Country.query.filter_by ( countryname=json_string[ 'country_id' ] ).first ( )
    if country is None:
        return "Country is not found!"
    if 'provincename' in json_string:
        province_name = Province.query.filter_by ( provincename=json_string[ 'provincename' ],
                                                   country_id=country.id ).first ( )
        if province_name is None:
            province = Province ( provincename=json_string[ 'provincename' ], country_id=country.id,
                                  coordinates=json_string[ 'coordinates' ] )
            db.session.add ( province )
            db.session.commit ( )
            return "Province created!"
        else:
            return "Province already exists!"
    if 'provinces' in json_string:
        for prov in json_string[ 'provinces' ]:
            prov_add = Province.query.filter_by ( provincename=prov[ 'provincename' ], country_id=country.id ).first ( )
            if prov_add is None:
                province = Province ( provincename=prov[ 'provincename' ], country_id=country.id,
                                      coordinates=prov[ 'coordinates' ] )
                db.session.add ( province )
        db.session.commit ( )
        return "Provinces created!"


@app.route ( '/add_area', methods=[ 'POST' ] )
def add_area():
    json_string = request.get_json ( force=True )
    if 'areas' in json_string:
        for a in json_string[ 'areas' ]:
            province = Province.query.filter_by ( provincename=a[ 'province_id' ] ).first ( )
            area_name = Area.query.filter_by ( areaname=a[ 'areaname' ], province_id=province.id ).first ( )
            if area_name is None:
                area = Area ( areaname=a[ 'areaname' ], province_id=province.id, coordinates=a[ 'coordinates' ] )
                db.session.add ( area )
        db.session.commit ( )
        return "Areas created!"


@app.route ( '/add_locality', methods=[ 'POST' ] )
def add_locality():
    json_string = request.get_json ( force=True )
    if 'area' in json_string:
        area = Area.query.filter_by ( areaname=json_string[ 'area_id' ] ).first ( )
    else:
        if 'localitys' in json_string:
            for loc in json_string[ 'localitys' ]:
                province = Province.query.filter_by ( provincename=loc[ 'province_id' ] ).first ( )
                area = Area.query.filter_by ( areaname=loc[ 'area_id' ] ).first ( )
                locality_name = Locality.query.filter_by ( localityname=loc[ 'localityname' ],
                                                           province_id=province.id ).first ( )
                if locality_name is None:
                    locality = Locality ( localityname=loc[ 'localityname' ], province_id=province.id,
                                          coordinates=loc[ 'coordinates' ], area_id=area.id )
                    db.session.add ( locality )
            db.session.commit ( )
            return "Localitys created!"


@app.route ( '/add_feature_loc', methods=[ 'POST' ] )
def add_feature_loc():
    json_string = request.get_json ( force=True )
    if 'features' in json_string:
        for curve in json_string[ 'features' ]:
            locality_name = Locality.query.filter_by ( localityname=curve[ 'locality_id' ] ).first ( )
            if locality_name is None:
                print ( 'Не нашел вот это, ', curve[ 'locality_id' ] )
            else:
                feature_name = Feature.query.filter_by ( featurename=curve[ 'feature_id' ] ).first ( )
                print ( locality_name.localityname )
                if feature_name is None:
                    return "Feature is not found!"
                val = curve[ 'values' ]
                for key in val.keys ( ):
                    feature_locality = FeatureLocality.query.filter (
                        and_ ( FeatureLocality.locality_id.like ( locality_name.id ),
                               FeatureLocality.feature_id.like ( feature_name.id ),
                               FeatureLocality.value.like ( val.get ( key ) ),
                               FeatureLocality.date.like ( key ) ) ).first ( )
                    if feature_locality is None:
                        feature = FeatureLocality ( locality_id=locality_name.id, feature_id=feature_name.id,
                                                    value=val.get ( key ), date=key )
                        db.session.add ( feature )
        db.session.commit ( )
        return "Features locality created!"


@app.route ( '/get_feature', methods=[ 'GET' ] )
def get_feature():
    features = Feature.query.all ( )
    res = [ ]
    for feature in features:
        category = Category.query.filter_by ( id=feature.category_id ).first ( )
        res.append ( {
            'feature_id': feature.id,
            'feature_name': feature.featurename,
            'category_name': category.categoryname,
            'dimension': feature.dimension
        } )
    return Response ( json.dumps ( {"amount features": len ( res ), "features": res} ),
                      content_type="application/json" )


@app.route ( '/get_area', methods=[ 'POST' ] )
def get_area():
    try:
        json_string = request.get_json ( force=True )
    except:
        json_string = None

    if json_string is None:
        areas = Area.query.all ( )
        res = [ ]
        for area in areas:
            province = Province.query.filter_by ( id=area.province_id ).first ( )
            res.append ( {
                'province_name': province.provincename,
                'area_id': area.id,
                'area_name': area.areaname,
                'coordinates': area.coordinates
            } )
        return Response ( json.dumps ( {"amount areas": len ( res ), "area": res} ), content_type="application/json" )
    else:
        if 'province_name' in json_string:
            province = Province.query.filter_by ( provincename=json_string[ 'province_name' ] ).first ( )
            areas = Area.query.filter_by ( province_id=province.id ).all ( )
            res = [ ]
            for area in areas:
                res.append ( {
                    'province_name': province.provincename,
                    'area_id': area.id,
                    'area_name': area.areaname,
                    'coordinates': area.coordinates
                } )
            return Response (
                json.dumps ( {"province name": province.provincename, "amount areas": len ( res ), "area": res} ),
                content_type="application/json" )


@app.route ( '/get_locality', methods=[ 'POST' ] )
def get_locality():
    try:
        json_string = request.get_json ( force=True )
    except:
        json_string = None
    if json_string is None:
        localitys = Locality.query.all ( )
        res = [ ]
        for locality in localitys:
            province = Province.query.filter_by ( id=locality.province_id ).first ( )
            area = Area.query.filter_by ( id=locality.area_id ).first ( )
            if area is None:
                areaname = ""
            else:
                areaname = area.areaname
            res.append ( {
                'locality_name': locality.localityname,
                'coordinates': locality.coordinates
            } )
        return Response ( json.dumps ( {"amount localitys": len ( res ), "locality": res} ),
                          content_type="application/json" )
    else:
        if 'province_name' in json_string:
            province = Province.query.filter_by ( provincename=json_string[ 'province_name' ] ).first ( )
            localitys = Locality.query.filter_by ( province_id=province.id ).all ( )
            res = [ ]
            for locality in localitys:
                area = Area.query.filter_by ( id=locality.area_id ).first ( )
                if area is None:
                    areaname = ""
                else:
                    areaname = area.areaname
                res.append ( {
                    'locality_name': locality.localityname,
                    'coordinates': locality.coordinates
                } )
            return Response ( json.dumps (
                {"province name": province.provincename, "amount localitys": len ( res ), "locality": res} ),
                content_type="application/json" )
        if 'area_name' in json_string:
            area = Area.query.filter_by ( areaname=json_string[ 'area_name' ] ).first ( )
            localitys = Locality.query.filter_by ( area_id=area.id ).all ( )
            res = [ ]
            for locality in localitys:
                areas = Area.query.filter_by ( id=locality.area_id ).first ( )
                if areas is None:
                    area_name = ""
                else:
                    area_name = areas.areaname
                res.append ( {
                    'locality_name': locality.localityname,
                    'coordinates': locality.coordinates
                } )
            return Response (
                json.dumps ( {"area name": area.areaname, "amount localitys": len ( res ), "locality": res} ),
                content_type="application/json" )


@app.route ( '/get_feature_locality', methods=[ 'POST' ] )
def get_feature_locality():
    json_string = request.get_json ( force=True )
    cities = json_string[ 'checkedCity' ]
    feat = json_string[ 'checkedFeature' ]
    yearMin = json_string[ 'yearMin' ]
    yearMax = json_string[ 'yearMax' ]
    percent = json_string[ 'percent' ]
    newArr = {
        'labels': [ ],
        'datasets': [ ],
        'title' : [],
    }
    for i in range ( int ( yearMin ), int ( yearMax ) + 1 ):
        newArr[ 'labels' ].append ( i )
    for el in feat:
        for x in cities:
            list = {}
            f = Feature.query.filter_by ( featurename=el ).first ( )
            l = Locality.query.filter_by ( localityname=x ).first ( )
            if l is None:
                return 'Locality not found'
            f_loc = FeatureLocality.query.filter_by ( feature_id=f.id, locality_id=l.id ) \
                .filter ( text ( "date>=" + str ( yearMin ) ) ) \
                .filter ( text ( "date<=" + str ( yearMax ) ) ) \
                .all ( )
            if el != 'Численность населения':
                if f.dimension == "Тыс. человек" or f.dimension == "Тысяч":
                    if percent == True:
                        pop = Feature.query.filter_by(featurename = "Численность населения").first()
                        data = [ ]
                        for item in f_loc:
                            population  = FeatureLocality.query.filter_by(feature_id = pop.id, locality_id = l.id)\
                            .filter(text("date = " + str(item.date))).first()
                            value = round(float(int(item.value)/int(population.value)) * 100, 3)
                            data.append(value)
                    else:
                        data = []
                        for item in f_loc:
                            data.append(int(item.value))
                if f.dimension =="Тонн/человека" or f.dimension == "Куб. м/человека":
                    pop = Feature.query.filter_by ( featurename="Численность населения" ).first ( )
                    data = [ ]
                    for item in f_loc:
                        population = FeatureLocality.query.filter_by ( feature_id=pop.id, locality_id=l.id ) \
                            .filter ( text ( "date = " + str ( item.date ) ) ).first ( )
                        value = round(int ( item.value ) / int ( population.value ), 3)
                        data.append ( value )
                if f.dimension == "на 100 000 человек населения":
                    data = []
                    for item in f_loc:
                        data.append(int(item.value))
            else:
                data = []
                for item in f_loc:
                    data.append(int(item.value))


            name = x
            list ['label'] = name
            list[ 'data' ] = data
            newArr ['title'] = f.dimension
            newArr[ 'datasets' ].append ( list )

    return Response ( json.dumps ( newArr ), content_type="application/json" )


@app.route ( '/init_map', methods=[ 'POST' ] )
def init_map():
    try:
        json_string = request.get_json ( force=True )
    except:
        json_string = None
    result = []
    values = [ ]
    if json_string:
        feat = json_string[ 'checkedFeature' ]
        year = json_string[ 'year' ]
        feature = Feature.query.filter_by(featurename = feat[0]).first()
        cities = Locality.query.all()
        for city in cities:
            featuresArr = FeatureLocality.query.filter_by ( feature_id=feature.id ) \
                .filter_by ( locality_id=city.id ) \
                .filter ( text ( "date=" + str ( year ) ) ).all ( )
            if(len(featuresArr) != 0):
                list = {}
                list['city'] = city.localityname
                coord = city.coordinates.split(', ')
                list['coord'] = coord
                data = {}
                if feature.dimension != "Численность населения":
                    if feature.dimension == "Тыс. человек" or feature.dimension == "Тысяч":
                        pop = Feature.query.filter_by ( featurename="Численность населения" ).first ( )
                        for item in featuresArr:
                            population = FeatureLocality.query.filter_by ( feature_id=pop.id, locality_id=city.id ) \
                                .filter ( text ( "date = " + str ( item.date ) ) ).first ( )
                            value = round ( float ( int ( item.value ) / int ( population.value ) ) * 100, 3 )
                            values.append(value)
                            data[item.date] = str(value) + ' %'
                    if feature.dimension == "на 100 000 человек":
                        for item in featuresArr:
                            values.append(float(item.value))
                            data[item.date] = str(item.value) + ' ' + feature.dimension
                    if feature.dimension == "Тонн/человека" or feature.dimension == "Куб. м/человека":
                        pop = Feature.query.filter_by ( featurename="Численность населения" ).first ( )
                        for item in featuresArr:
                            population = FeatureLocality.query.filter_by ( feature_id=pop.id, locality_id=city.id ) \
                                .filter ( text ( "date = " + str ( item.date ) ) ).first ( )
                            value = round ( float ( int ( item.value ) / int ( population.value ) ) * 100, 3 )
                            if value > 7000000:
                                print(city.id)
                            values.append ( value )
                            data[ item.date ] = str(item.value) + ' ' + feature.dimension

                list['values'] = data
                result.append(list)
        maxVal = max(values)
        minVal = min(values)
        for item in result:
            for key in item['values'].keys():
                if feature.dimension == "Тыс. человек" or feature.dimension == "Тысяч":
                    val = float(item['values'][key].replace(' %',''))
                elif feature.dimension == "на 100 000 человек":
                    val = float(item['values'][key].replace(' на 100 000 человек',''))
                elif feature.dimension == "Тонн/человека" or feature.dimension == "Куб. м/человека":
                    val = float ( item[ 'values' ][ key ].replace ( ' ' + feature.dimension, '' ) )
                color = rgb_price(val,minVal,maxVal)
                item['color'] = color

    return Response ( json.dumps ( result ), content_type="application/json" )

@app.route ( '/get_report', methods=[ 'POST' ] )
def get_report():
    path = os.path.join ( os.path.abspath ( os.getcwd ( ) ), 'report.xlsx' )
    try:
        return send_file ( path, attachment_filename="report.xlsx", as_attachment=True )
    except Exception as e:
        return str ( e )


@app.route ( '/prepare_report', methods=[ 'POST' ] )
def prepare_report():
    json_string = request.get_json ( force=True )
    wb = Workbook ( )
    dest_filename = 'report.xlsx'

    ws1 = wb.active
    ws1.title = "Отчет"
    ws1[ 'B1' ] = 2010
    ws1[ 'C1' ] = 2011
    ws1[ 'D1' ] = 2012
    ws1[ 'E1' ] = 2013
    ws1[ 'F1' ] = 2014
    ws1[ 'G1' ] = 2015
    ws1[ 'H1' ] = 2016
    ws1[ 'I1' ] = 2017
    index = 2
    for el in json_string:
        ws1[ 'A' + str ( index ) ] = el[ 'name' ]
        data = el[ 'data' ]
        ws1[ 'B' + str ( index ) ] = data.get ( '2010' )
        ws1[ 'C' + str ( index ) ] = data.get ( '2011' )
        ws1[ 'D' + str ( index ) ] = data.get ( '2012' )
        ws1[ 'E' + str ( index ) ] = data.get ( '2013' )
        ws1[ 'F' + str ( index ) ] = data.get ( '2014' )
        ws1[ 'G' + str ( index ) ] = data.get ( '2015' )
        ws1[ 'H' + str ( index ) ] = data.get ( '2016' )
        ws1[ 'I' + str ( index ) ] = data.get ( '2017' )
        index += 1
    wb.save ( filename=dest_filename )
    return Response ( json.dumps ( 'Готово' ), content_type="application/json" )
