import tweepy

class ShowFriendship:    
    
    def __init__(self, api):
        """
        Initializes the object given previously authed api
        """
        self._api = api
    

    def get_friendship(self, sourceid, targetid):
        """
        Describes the kind of friendship given
        @sourceid  the source profile id
        @targetid  the target profileid
        
        @returns a dictionary
        """
        friendship = self._get_friendship_obj(sourceid, targetid)
        friendship_type = self._detect_friendship_type(friendship)
        return self._get_output(sourceid, targetid, friendship_type)
    
    
    def _get_friendship_obj(self, sourceid, targetid):
        """
        Gets the friendship object and returns it
        """
        friendship = self._api.show_frienship(sourceid, targetid)
        return friendship
    
    
    def _detect_friendship_type(self, friendship):
        """
        Detect which kind of friendship exists between users
        """
        if not friendship[0].following and not friendship[0].followed_by:
            return "none"
        elif not friendship[0].following and friendship[0].followed_by:
            return "r_l"
        elif friendship[0].following and not friendship[0].followed_by:
            return "l_r"
        else:
            return "bi"
    
    
    def _get_output(self, sourceid, targetid, kind_of_friendship):
        """
        Builds the output dictionary
        """
        return {
            "source_id": sourceid,
            "target_id": targetid,
            "friendship": kind_of_friendship
        }

    