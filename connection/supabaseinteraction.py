from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


async def send_event(event: dict):
    supabase.table("event").insert(event).execute()


async def get_user_rsvp(uuid):
    return supabase.table("RSVP").select("eventID").eq("userID", uuid).execute().data


async def set_rsvp(rsvp_info):
    supabase.table("RSVP").upsert(rsvp_info).execute()


async def get_user_uuid(**kwargs):
    # Given discord or telegram userID, returns the user uuid.
    # Only takes either TeleID or DiscID, and chooses discord ID over Telegram ID if both are given.

    # Pythonic way
    for arg in kwargs:
        if arg in ["DiscID", "TeleID"]:
            return supabase.table("Profile").select("id").eq(arg, kwargs[arg]).execute().data[0]['id']

    #Trivial way
    # if "TeleID" in kwargs and "DiscID" in kwargs:
    #     raise Exception("Provide only one of either Telegram ID or Discord ID!")
    # elif "TeleID" in kwargs:
    #     return supabase.table("Profile").select("id").eq("TeleID", kwargs["TeleID"]).execute().data[0]['id']
    # elif "DiscID" in kwargs:
    #     return supabase.table("Profile").select("id").eq("DiscID", kwargs["DiscID"]).execute().data[0]['id']
    # else:
    #     raise Exception("Please provide a Telegram or Discord kwargs as argument!")


async def get_all_events():
    return supabase.table("event").select("*").execute().data


async def get_user_events(profileid):
    # for arg in kwargs:
    #     if arg == "ProfileID":
    #         return supabase.table("event").select("*").eq("creatorID", kwargs["ProfileID"]).execute().data
    #     elif arg in ["TeleID", "DiscID"]:
    #         return get_user_events(ProfileID=get_user_uuid(arg=kwargs[arg]))
    return supabase.table("event").select("*").eq("creatorID", profileid).execute().data


async def get_teleuser_events(TeleID):
    return get_user_events(get_user_uuid(TeleID=TeleID)).data


async def get_discuser_events(DiscID):
    return get_user_events(get_user_uuid(DiscID=DiscID)).data

if __name__ == "__main__":
    print(get_user_uuid(DiscID=123))
    print(supabase.table("event").select('starttime').execute())
    print(type(supabase.table("event").insert({'activity': 'testinsert', 'starttime': '2022-06-23T12:14:33+00:00'}).execute()))