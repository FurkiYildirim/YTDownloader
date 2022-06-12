from sys import argv
from pytube import YouTube
from os import path, rename


def args():
    """commnads

    --link
    --help
    --setname

    """
    commands = ['--help', '--link', '--loc', '--res', '--filetype']
    argLine = argv[1::]

    # commands_with_parameter = []  # [(command, paramter)...]
    commands_with_parameterDict = {}  # {command: parameter}

    for param in argLine:
        if param in commands:
            command = commands[commands.index(param)]
            if command == "--help":
                parameter = None
            else:
                parameter = argLine[argLine.index(param) + 1]

            commands_with_parameterDict.update({command: parameter})

    return commands_with_parameterDict


argsFromCLine = args()
downloads_path = "downloads/"

if argsFromCLine.get('--loc') != None:
    downloads_path = argsFromCLine.get('--loc')

print(downloads_path)




class YtDownloader:
    def __init__(self):
        try:
            if argsFromCLine.get('--help'):
                self.help()
                exit()
            location = downloads_path
            link = argsFromCLine.get('--link')
            res = argsFromCLine.get('--res')
            filetypee = argsFromCLine.get('--filetype')
            self.download(link=link, resolution=res, location=location, fileType=filetypee)
        except Exception as err:
            print(f'error: {err}')

    def help(self):
        return ("""
        [TR]
        --help : Komutların ne işe yaradığını gösterir
        --link : İndirmek istediğin videonun linki  (--links parametresi kullanılamaz)
        --links: İndirmek istediğin videoların .txt dosyası (--link parametresi kullanılamaz)
        --loc  : İndirme konumu 
        --filetype : indirilecek videonun tipi (mp4/mp3) 
        
        -----------
        
        TXT Dosya formatı
        örnek:
        link | type(mp4/mp3)| resolution(high/low)
        link | type(mp4/mp3)| resolution(high/low)
        link | type(mp4/mp3)| resolution(high/low)

        [EN]
        coming soon
        """)

    def download(self, link: str, resolution: str, fileType: str, location: str):
        """

        :param linkType: "link" or "txt file"
        :param resolution: "high","low"
        :param fileType: mp4/mp3
        :return:
        """
        links = []
        if ".txt" in link:
            with open(link, "r") as fileObj:
                datas = [i.replace('\n', '') for i in fileObj.readlines()]
                for link in datas:
                    link = link.split('|')
                    links.append((link[0],link[1],link[2]))  # [(link, type, res)]
        else:
            links.append((link, fileType, resolution))


        for link in links:
            linkt = link[0]
            fileType = link[1]
            resolution = link[2]
            video = YouTube(linkt)
            if fileType == "mp4":
                if resolution == "high":
                    video = video.streams.get_highest_resolution()
                if resolution == "low":
                    video = video.streams.get_lowest_resolution()

                video.download(downloads_path)
                print(f'{video.title} downloaded | type = mp4 Res = {resolution} |')

            if fileType == "mp3":
                video = video.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=location)

                # save the file
                base, ext = path.splitext(out_file)
                new_file = base + '.mp3'
                rename(out_file, new_file)
                print(f'{video.title} downloaded | type = mp3 |')

YtDownloader()
