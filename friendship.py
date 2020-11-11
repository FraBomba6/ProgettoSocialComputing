import tweepy 
from tweepy import API

def get_friendship(sourceid, targetid, api):

    kind = ""
    
    friendship = api.show_friendship(source_id=sourceid, target_id=targetid)

    if not friendship[0].following and not friendship[0].followed_by:
        kind = "none"
    elif not friendship[0].following and friendship[0].followed_by:
        kind = "r_l"
    elif friendship[0].following and not friendship[0].followed_by:
        kind = "l_r"
    else:
        kind = "bi"
    
    return {
            "source_id": sourceid,
            "target_id": targetid,
            "friendship": kind
        }