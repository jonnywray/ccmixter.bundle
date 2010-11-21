
PREFIX      = "/music/ccmixter"

BASE_PAGE   = "http://dig.ccmixter.org/%soffset=%d"
PAGE_SIZE	= 10
####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PREFIX, MainMenu, "ccMixter", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="audio")
  MediaContainer.art = R('art-default.jpg')
  MediaContainer.title1 = 'ccMixter'
  DirectoryItem.thumb=R("icon-default.png")
  
    
########################################################################################################
def MainMenu():
    dir = MediaContainer() 
    
    dir.Append(Function(DirectoryItem(SectionTracks, "Editors' Picks"), path="picks?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Popular"), path="popular?"))
    
    dir.Append(Function(DirectoryItem(SectionTracks, "Vocals Music Safe for Podcasts"), path="podcast_music?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Instrumental Music for Film and Video"), path="music_for_film_and_video?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Electro Instrumental Music for Games"), path="music_for_games?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Acoustic-ish Instrumental Coffeeshop Music"), path="coffeeshop_music?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Party Music"), path="party_music?"))
    dir.Append(Function(DirectoryItem(SectionTracks, "Chill Cubicle Music"), path="cubicle_music?"))
    
    dir.Append(Function(InputDirectoryItem(Search, title="Search ...", thumb=R("icon-search.png"), prompt="Search cc.mixter back-catalogue and discover new music")))
    return dir
   
#######################################################################################################
def Search(sender, query):
	path = "dig?dig-query="+String.Quote(query)+"&"
	return SectionTracks(sender, path)
  
#######################################################################################################
def SectionTracks(sender, path, offset=0):
    dir = MediaContainer(viewGroup="Details", title2=sender.itemTitle)
    url = BASE_PAGE % (path, offset)
    Log("Fetching tracks from "+url)
    content = HTTP.Request(url).content
    prefix = content.find('query_results.call')
    suffix = content.find('</script>', prefix)
    start = content.find('[', prefix, suffix)
    end = content.rfind(']', prefix,suffix) + 1
    queryResults = JSON.ObjectFromString(content[start:end])
    for track in queryResults:
    
    	title = track['upload_name']
    	subtitle = None
    	if 'featuring' in track['upload_extra']:
    		subtitle =  track['upload_extra']['featuring']
    		if subtitle != None and len(subtitle) > 0:
    			subtitle = "Featuring "+subtitle
    	audioFile = track['files'][0]['download_url']
    	summary = track['upload_description_plain']
    	thumb = track['user_avatar_url']
    	artist = track['user_name']
    	duration = track['files'][0]['file_format_info']['ps']
    	formattedDuration = FormatDuration(duration)
    	dir.Append(TrackItem(audioFile, title, artist, duration=formattedDuration, subtitle = subtitle, summary=summary, thumb=thumb))
    if len(queryResults) == PAGE_SIZE:
    	dir.Append(Function(DirectoryItem(SectionTracks, "More ..."), path=path, offset=offset+10))
    return dir

#########################################################
def FormatDuration(duration):
    tokens = duration.split(':')
    duration = int(tokens[-1])
    if len(tokens) > 1:
    	duration = duration + 60*int(tokens[-2])
    if len(tokens) > 2:
    	duration = duration + 60*60*int(tokens[-3])
    return duration*1000

    