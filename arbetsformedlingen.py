import xml.etree.ElementTree as ET
import requests
import urllib2

API_URL = 'http://api.arbetsformedlingen.se/platsannons/matchning'
API_ROOT_URL = 'http://api.arbetsformedlingen.se/platsannons/'


def _request_listings(page=1, lanid=1):
    params = {
        'lanid': lanid,
        'sida': page,
    }
    headers = {
        'Accept': 'application/xml',
        'Accept-Language': 'en-US',
    }
    req = requests.get(API_URL, params=params, headers=headers)
    return req.text


def _request_listing(id):
    headers = {
        'Accept': 'application/xml',
        'Accept-Language': 'en-US',
    }

    req = requests.get(API_ROOT_URL + id, headers=headers)

    return req.text


def _parse_listings_xml_string(xml_string):
    xml_root = ET.fromstring(xml_string.encode('utf-8'))
    listings = []
    for listing in xml_root.findall('matchningdata'):
        id = listing.find('annonsid').text
        listing_xml = _request_listing(id)
        listings.append(listing_xml)
    return listings


def _parse_listing_xml_string(xml_string):
    xml_root = ET.fromstring(xml_string.encode('utf-8'))
    listing_xml = xml_root.find('annons')
    id = listing_xml.find('annonsid').text
    try:
        title = listing_xml.find('annonsrubrik').text
    except:
        title = ''

    try:
        content = listing_xml.find('annonstext').text
    except:
        content = ''
    try:
        location = xml_root.find('arbetsplats').find('postort').text
    except:
        location = ''

    listing = {
        'source_id': id,
        'title': title,
        'location': location,
        'content': content,
    }
    return listing


def _parse_company_xml_string(xml_string):
    xml_root = ET.fromstring(xml_string.encode('utf-8'))
    listing_xml = xml_root.find('arbetsplats')
    try:
        listing_id = xml_root.find('annons').find('annonsid').text
        logo_url = 'http://api.arbetsformedlingen.se/platsannons/{0}/logotyp'.format(listing_id)
    except:
        listing_id = ""
        logo_url = ""

    try:
        id = (listing_xml.find('arbetsplatsnamn').text).encode('utf-8')
    except:
        id = ''
    try:
        title = listing_xml.find('arbetsplatsnamn').text
    except:
        title = ''
    company = {
        'source_id': id,
        'title': title,
        'logo_url': logo_url
    }
    return company


def _parse_profession_xml_string(xml_string):
    xml_root = ET.fromstring(xml_string.encode('utf-8'))
    listing_xml = xml_root.find('annons')
    try:
        id = listing_xml.find('yrkesid').text
    except:
        id = ""
    try:
        title = listing_xml.find('yrkesbenamning').text
    except:
        title
    profession = {
        'source_id': id,
        'title': title,
    }
    return profession


def get_listings(page=1, lanid=1):
    listings = []
    listingsxml = _request_listings(page, lanid)
    listings_xml = _parse_listings_xml_string(listingsxml)
    for listing in listings_xml:
        company_object = _parse_company_xml_string(listing)
        profession_object = _parse_profession_xml_string(listing)
        listing_object = _parse_listing_xml_string(listing)
        listing_object['profession'] = profession_object
        listing_object['company'] = company_object
        listings.append(listing_object)
    return listings
