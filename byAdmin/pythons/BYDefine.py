import os


class BYDefine:
    # CodeRootPath = str(os.path.join(os.path.dirname(os.path.dirname(__file__)), "../"))
    CodeRootPath = os.path.dirname(os.path.dirname(__file__))
    LoggingPath = CodeRootPath + "/logs/"
    ResourcePath = CodeRootPath + "/resource/"
    TemplatesPath = CodeRootPath + "/templates/"
    ModuleFilesPath = CodeRootPath + "/modules/"
    StaticFilesPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    ContentsPath = StaticFilesPath + "/contents/"
    PreviewFilePath = StaticFilesPath + '/preview.html'
    BieyangDomain = 'https://fifth-ave-api.borderxlab.com/'


