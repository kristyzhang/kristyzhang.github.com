import os
import json
import urllib

from BYDefine import BYDefine
from FileManager import FileManager
import urllib2
from PIL import Image
from PIL import ImageFile
from string import Template
from tornado import template

class ContentsManager:

    @staticmethod
    def creat_all_dictory():
        FileManager.make_dir(BYDefine.ResourcePath)
        FileManager.make_dir(BYDefine.ContentsPath)
        FileManager.make_dir(BYDefine.LoggingPath)

    @staticmethod
    def append_content(paras):
        FileManager.touch_file(BYDefine.ContentsPath)
        jsonString = ContentsManager.content_from_file()
        content = []
        if len(jsonString):
            content = json.loads(jsonString)

        content.append(paras)
        FileManager.write_string_to_file(BYDefine.ContentsPath, json.dumps(content))

    @staticmethod
    def generate_content(contents_path, file, parameters):
        FileManager.make_dir(contents_path)
        FileManager.touch_file(contents_path + file)
        FileManager.write_string_to_file(contents_path + file, json.dumps(parameters))

    @staticmethod
    def content_from_file():
        FileManager.touch_file(BYDefine.ContentsPath)
        return FileManager.read_file(BYDefine.ContentsPath)

    @staticmethod
    def active_contents_list():
        deals = ContentsManager.contents_list()
        outdate_deals = []
        for index, deal in enumerate(deals):
            if deal['expire'] == '1':
                outdate_deals.append(deal)
            elif len(deal['custom_url']) == 0:
                deal['custom_url'] = ContentsManager.create_deep_link(deal)

            deal['share_link'] = ContentsManager.creat_share_link(deal, BYDefine.BieyangDomain)
            deals[index] = deal

        for i, d in enumerate(outdate_deals):
            deals.remove(d)

        return deals

    @staticmethod
    def contents_list():
        contents_list = []

        for item in os.listdir(BYDefine.ContentsPath):
            if os.path.isdir(os.path.join(BYDefine.ContentsPath, item)):
                jsonfile = BYDefine.ContentsPath + item + "/" + item + ".json"
                jsonString = FileManager.read_file(jsonfile)
                deal = json.loads(jsonString)
                deal['id'] = str(item)
                contents_list.append(deal)

        return contents_list

    @staticmethod
    def content_by_id(deal_id):
        deal = {}
        jsonfile = BYDefine.ContentsPath + deal_id + "/" + deal_id + ".json"
        if os.path.exists(jsonfile):
            jsonString = FileManager.read_file(jsonfile)
            deal = json.loads(jsonString)
            if 'id' not in deal:
                deal['id'] = deal_id

        return deal

    @staticmethod
    def create_deep_link(deal):
        deep_link = 'cid=' + deal['cid'] + '&ctitle=' + deal['title']

        for merchant_id in deal['merchants']:
            deep_link = deep_link + '&m=' + merchant_id

        for brand_id in deal['brands']:
            deep_link = deep_link + '&b=' + brand_id

        if deal['discount']:
            deep_link = deep_link + '&l=on_sale,clearance'

        deep_link = urllib.quote(deep_link.encode('utf8'))
        return deep_link

    @staticmethod
    def creat_share_link(deal, domain):
        share_link_url = deal["custom_url"]
        if len(share_link_url) > 0:
            prefix = 'static/curation/'
            share_link_url = prefix + share_link_url + '?&sdesciption=' + deal['title']
            share_link_url = share_link_url + '&simage=' + domain + prefix + 'contents/' + deal['id'] + '/thumb' + deal['image']
            share_link_url = urllib.quote(share_link_url.encode('utf8'))

        return share_link_url

    @staticmethod
    def removeOldImages(deal_id):
        deal_folder = BYDefine.ContentsPath + deal_id + '/'

        deal = ContentsManager.content_by_id(deal_id)
        image_name = deal.get('image', '')
        if len(image_name) > 0:
            thumb_name = 'thumb' + image_name
            image_path = deal_folder + image_name
            thumb_path = deal_folder + thumb_name
            FileManager.remove_file(image_path)
            FileManager.remove_file(thumb_path)

    @staticmethod
    def createThumbnail(deal_id):
        deal_folder = BYDefine.ContentsPath + deal_id + '/'

        deal = ContentsManager.content_by_id(deal_id)
        image_name = deal['image']
        thumb_name = 'thumb' + image_name
        image_path = deal_folder + image_name
        thumb_path = deal_folder + thumb_name

        ImageFile.LOAD_TRUNCATED_IMAGES = True

        image = Image.open(image_path)
        orignal_width, original_height = image.size
        new_width = 300
        new_height = new_width * original_height / orignal_width

        image.thumbnail((new_width, new_height), Image.BILINEAR)
        image.save(thumb_path)

    @staticmethod
    def generate_html(content):
        FileManager.save_file(BYDefine.PreviewFilePath, content)
        html_str = FileManager.read_file(BYDefine.PreviewFilePath)
        html_str = html_str.replace("/static/", "")
        FileManager.write_string_to_file(BYDefine.PreviewFilePath, html_str)

    @staticmethod
    def generate_sub_html(deal_id, domain):
        sub_template = FileManager.read_file(BYDefine.TemplatesPath + 'subpage.html')
        deal = ContentsManager.content_by_id(deal_id)
        deal['deeplink'] = ContentsManager.create_deep_link(deal)
        deal['desc'] = "<br />".join(deal['desc'].split("\r\n"))
        deal['sharelink'] = ContentsManager.creat_share_link(deal, domain)
        t = Template(sub_template)
        sub_page_html = t.substitute(deal)
        save_path = BYDefine.ContentsPath + deal_id + '/' + deal_id + '.html'
        FileManager.write_string_to_file(save_path, sub_page_html)
