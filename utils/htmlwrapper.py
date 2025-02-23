def chatEventMsgtoString(fragments ):
    htmlPrintable =[]
    for frags in fragments:
        if (frags.type) == "text":
            htmlPrintable.append({1: (frags.text).strip()})

        elif frags.type =="emote":
            emoteId = frags.emote.id 
            emoteSetId = frags.emote.emote_set_id
            emoteOwnerId = frags.emote.owner_id
            emotePart = ""
   

            emote_url = "https://static-cdn.jtvnw.net/emoticons/v2/***/default/dark/1.0"
            emote_url = emote_url.replace("***", str(emoteId))

            #await checkEmotes(emoteOwnerId, emoteSetId, emoteId)

            emotePart = "<img src="+emote_url+"></img>"
             
            htmlPrintable.append({0:emotePart})

    return htmlPrintable