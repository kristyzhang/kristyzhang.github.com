import json
import time

import tornado.ioloop
import tornado.web
import tornado.template
import os
from tornado.options import options

from FileManager import FileManager
from BYDefine import BYDefine
from ContentsManager import ContentsManager


class DealRowModule(tornado.web.UIModule):
    def render(self, deal):
        return self.render_string(BYDefine.ModuleFilesPath + 'deal_row.html', deal=deal)

class CategoryRowModule(tornado.web.UIModule):
    def render(self, category, checked):
        return self.render_string(BYDefine.ModuleFilesPath + 'category_row.html', category=category, checked=checked)

class BrandRowModule(tornado.web.UIModule):
    def render(self, brand, checked):
        return self.render_string(BYDefine.ModuleFilesPath + 'brand_row.html', brand=brand, checked=checked)

class MerchantRowModule(tornado.web.UIModule):
    def render(self, merchant, checked):
        return self.render_string(BYDefine.ModuleFilesPath + 'merchant_row.html', merchant=merchant, checked=checked)

class ContentListRowModule(tornado.web.UIModule):
    def render(self, deal):
        return self.render_string(BYDefine.ModuleFilesPath + 'content_list_row.html', deal=deal)

class NaviModule(tornado.web.UIModule):
    def render(self, page):
        return self.render_string(BYDefine.ModuleFilesPath + 'navi.html', page=page)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.redirect('/deals')
        # id = self.get_argument('id', '')
        # password = self.get_argument('password', '')
        # if id == 'admin' and password == 'by2015':
        #     self.set_secure_cookie("username", self.get_argument(id))
        #     self.redirect('/deals')
        # else:
        #     self.redirect('/')

class SyncHandler(BaseHandler):
    def get(self):
        filename = BYDefine.PreviewFilePath
        self.set_header('Content-Type', "text/csv")
        self.set_header('Content-Disposition',
                        "attachment; filename=\"home.html\"")
        self.set_header('Content-Length', os.path.getsize(filename))
        with open(filename, 'rb') as fp:
            self.write(fp.read())


class PreviewHandler(BaseHandler):
    def get(self):
        ordered_items = []
        if self.get_arguments('ordered_items') and self.get_arguments('ordered_items')[0]:
            ordered_items = self.get_arguments('ordered_items')[0].split(',')
            ordered_items = [int(i) for i in ordered_items if i]
        if not ordered_items:
            ordered_items = json.loads(FileManager.read_file(BYDefine.ResourcePath + 'content_list.json'))

        deals = Sort(ordered_items, ContentsManager.active_contents_list())

        self.render('curation_home_base.html', deals=deals)
        content = '[' + ','.join([d['id'] for d in deals]) + ']'
        FileManager.save_file(BYDefine.ResourcePath + 'content_list.json', content)

    def write(self, chunk):
        ContentsManager.generate_html(chunk)
        super(PreviewHandler, self).write(chunk)

def Sort(saved, deals):
    sorted_deals = []
    left_over = list(deals)

    for item in saved:
        for deal in left_over:
            if item == int(deal['id']):
                sorted_deals.append(deal)
                left_over = [d for d in left_over if not int(d['id']) == item]
                break
    sorted_deals.extend(left_over)
    return sorted_deals


class DealsHandler(BaseHandler):
    def post(self):
        self.clear()
        self.set_status(400)
        self.finish("<html><body>Post is not supported</body></html>")

    def get(self):
        saved = json.loads(FileManager.read_file(BYDefine.ResourcePath + 'content_list.json'))
        deals = Sort(saved, ContentsManager.contents_list())
        self.render('deals.html', deals=deals)

class DealHandler(BaseHandler):
    def get(self, deal_id):
        brands = json.loads(FileManager.read_file(BYDefine.ResourcePath + 'brand_list.json'))
        merchants = json.loads(FileManager.read_file(BYDefine.ResourcePath + 'merchant_list.json'))
        categories = json.loads(FileManager.read_file(BYDefine.ResourcePath + 'category_list.json'))
        deal = ContentsManager.content_by_id(deal_id)

        self.render('deal.html', brands=brands, merchants=merchants, categories=categories, deal=deal)

    def post(self, deal_id):
        timeStamp = str(int(time.time()))
        if not deal_id:
            deal_id = timeStamp

        requestParameters = {}

        requestParameters['merchants'] = self.get_arguments('merchants[]')
        requestParameters['brands'] = self.get_arguments('brands[]')
        requestParameters['title'] = self.get_argument('title', '').replace(' ', '')
        requestParameters['date'] = self.get_argument('date', '')
        requestParameters['desc'] = self.get_argument("desc", '')
        requestParameters['expire'] = self.get_argument('expire', '')
        requestParameters['discCode'] = self.get_argument('discCode', '')
        requestParameters['image'] = self.get_argument('image', '')
        requestParameters['cid'] = self.get_argument('cid', 'all')
        requestParameters['discount'] = int(self.get_argument('discount', 1))
        requestParameters['id'] = deal_id
        requestParameters['custom_url'] = self.get_argument('custom_url', '')

        if not len(requestParameters['custom_url']):
            requestParameters['custom_url'] = 'contents/'+ deal_id + '/' + deal_id + '.html'

        imageName = ''
        # save image

        if self.request.files.get('image'):
            ContentsManager.removeOldImages(deal_id)
            image = self.request.files['image'][0]
            imageExtension = image['filename'].split('.')[1]
            imageName = timeStamp + '.' + imageExtension

        contentPath = BYDefine.ContentsPath + deal_id + '/'
        if len(imageName):
            requestParameters['image'] = imageName
        else:
            old_deal = ContentsManager.content_by_id(deal_id)
            requestParameters['image'] = old_deal.get('image', '')

        print(requestParameters)

        #save json file

        contentFileName = deal_id + ".json"
        ContentsManager.generate_content(contentPath, contentFileName, requestParameters)

        if len(imageName):
            FileManager.make_dir(contentPath)
            output_file = open(contentPath + imageName, 'wb')
            output_file.write(image['body'])
            ContentsManager.createThumbnail(deal_id)

        if deal_id + '.html' in requestParameters['custom_url']:
            ContentsManager.generate_sub_html(deal_id, BYDefine.BieyangDomain)
        self.write("Post Succeed")

application = tornado.web.Application(
    handlers=[
        (r"/", DealsHandler),
        (r"/deal/(\d*)", DealHandler),
        (r"/deals", DealsHandler),
        (r"/login", LoginHandler),
        (r"/preview", PreviewHandler),
        (r"/sync", SyncHandler),
    ],
    template_path=BYDefine.TemplatesPath,
    static_path=BYDefine.StaticFilesPath,
    cookie_secret="4?hW|;H_BQB$q|DdBq=ACw!aM9Idpj,#",
    login_url="/login",
    ui_modules={'DealRowModule': DealRowModule,
                'NaviModule': NaviModule,
                'CategoryRowModule': CategoryRowModule,
                'BrandRowModule': BrandRowModule,
                'MerchantRowModule': MerchantRowModule,
                'ContentListRowModule': ContentListRowModule},
    debug=True
)

if __name__ == "__main__":
    ContentsManager.creat_all_dictory()
    options.log_file_prefix = BYDefine.LoggingPath
    application.listen(9527)
    tornado.ioloop.IOLoop.current().start()

