import scrapetube 

class ScrapeYT_Channel:
    def __init__(self, limit=10, content_type="videos") -> None:
        self.yt_url = None 
        self.limit = 50
        self.content_type = content_type 
        self.selected_keys = ['videoId', 'thumbnail', 'title', 'descriptionSnippet', 'richThumbnail', 'headline']
        self.link_template = "https://www.youtube.com/watch?v="
        # self.get_vid_info, isSuccess = self.get_channel_vids_info()
        # if not isSuccess

    def get_yt_url(self, url):
        self.yt_url = url 

    def get_channel_vids_info(self):
        if self.yt_url is None:
            return "Enter a url", False 
        if self.content_type == "search":
            videos = scrapetube.get_search(query=self.yt_url,
                                           limit=self.limit,
                                           results_type="video")
        else:
            videos = scrapetube.get_channel(channel_username=self.yt_url,
                                            limit=self.limit,
                                            content_type=self.content_type) 
        catalog = [] 
        try:
            for vid in videos:
                info = {key: vid[key] for key in self.selected_keys if key in vid}
                if "videoId" in info:
                    info["targetId"] = info["videoId"]
                    info["videoId"] = self.link_template + info["videoId"]
                else:
                    info["targetId"] = None
                    info["videoId"] = None
                catalog.append(info)

            return catalog, True 
        except Exception as e:
            return 'Check link again', False
