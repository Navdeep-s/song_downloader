
import warnings
import requests,bs4
import os
import sys
import threading


warnings.filterwarnings("ignore")
quality_set=True
quality =0


def change_format(sti):
    new_sti = "-".join((sti.lower().split(" ")))
    return new_sti


def get_root(url):
    root = ""
    count=0
    for k in url:
        if(k=="/"):
            count = count+1
        if(count==3):
            break
        root=root+k
    return root




url = "https://djpunjab.fm/punjabi-music/ammi-kamal-khan-mp3-song-294966.html#gsc.tab=0"


path_file = open("path.txt","r")
path=path_file.read()
path_file.close()

def download_song_from_link(url):
    os.chdir(path)
    k = open("current_song", "r")
    value = int(k.read())
    new_value = value + 1
    k.close()
    k = open("current_song", "w")
    k.write(str(new_value))
    print(value)
    k.close()

    print("Downloading...")
    res = requests.get(url,verify=False)

    imageFile = open("song{}.mp3".format(value), "wb")
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    print("Done")
    # webbrowser.open(url)



#   takes the url of artists page
#   return list of tupples containing name and link of the album or sings songs
#   method select_from_the_album should be aplied to each url
def get_artists_songs(url):



    root = get_root(url)

    res = requests.get(url,verify=False)

    soup = bs4.BeautifulSoup(res.text,features="html.parser")

    y=soup.select(".songs")[0]


    # print(y)
    i=y.select("p a")

    songs=[]
    for u in i:
        name = u.getText()
        href = root+u.get("href")
        songs.append((name, href))

    return (songs)




# takes the url of a particular album or song
# return the list of tuples of names and links of all songs in that particular album
# method get_quality should be applied to this
def select_from_album(url):
    res=requests.get(url,verify=False)

    root=get_root(url)

    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    soup = bs4.BeautifulSoup(res.text,features="html.parser")


    names = []


    y=soup.select(".dj")
    for k in y:
        text=k.getText()

        if(text.startswith("48Kb")):
            break

        href=root+k.findChild().get("href")
        names.append((text, href))
    return (names)

def get_quality(url):
    res=requests.get(url,verify=False)
    soup = bs4.BeautifulSoup(res.text,features="html.parser")

    k=soup.select("p a[href]")
    download_elem=[]
    for u in k:
        p=u.getText()
        if p.startswith("Download") :
            size = u.parent.getText()
            href  = u.get("href")

            download_elem.append((size,href))

    return download_elem


# print(get_artists_songs(url))

def get_top_songs():
    url = "https://djpunjab.fm/page/top20.html?type=week#gsc.tab=0"
    root = get_root(url)
    res = requests.get(url,verify=False)
    soup = bs4.BeautifulSoup(res.text,features="html.parser")
    y =soup.select("li p")

    collection= []

    for u in y:
        name = u.getText()
        href = root+u.findChild().get("href")
        collection.append((name, href))
    return collection

# print(get_top_songs())


def find_artist(sti):


    new_sti = "+".join((sti.lower().split(" ")))
    url = "https://djpunjab.fm/punjabi_music/searchbycat.php?search={}&type=artist&cat_id=1&submit=Submit#gsc.tab=0".format(new_sti)
    root = get_root(url)
    res = requests.get(url,verify=False)

    try:
        res.raise_for_status()

    except Exception as exc:
        print('There was a problem: %s' % (exc))

    soup = bs4.BeautifulSoup(res.text, features="html.parser")
    u = soup.select(".dj")

    collection = []
    for k in u:
        name = k.getText()
        if(name.endswith("Home")):
            break
        href = root + k.findChild().get("href")
        collection.append((name, href))
    return collection





# print(get_quality("https://djpunjab.fm/punjabi-music/ammi-kamal-khan-mp3-song-294966.html#gsc.tab=0"))


def search_song(sti):
    new_sti = "+".join((sti.lower().split(" ")))
    url = "https://djpunjab.fm/punjabi_music/searchbycat.php?search={}&type=album&cat_id=1&submit=Submit#gsc.tab=0".format(new_sti)
    root = get_root(url)
    res = requests.get(url,verify=False)

    try:
        res.raise_for_status()

    except Exception as exc:
        print('There was a problem: %s' % (exc))

    soup = bs4.BeautifulSoup(res.text,features="html.parser")
    u=soup.select(".style1")

    collection=[]
    for k in u:
        y = k.parent
        name = y.getText()
        href = root+y.findChild().get("href")
        collection.append((name, href))
    return collection

def search_song_handler():
    global quality_set
    y=input("Type the name of the song\n")

    songs=search_song(y)

    return songs

def song_selection_hanlder(songs):
    if (len(songs) == 0):
        y=len(songs)
        print("there is no song named {} in out database".format(y))
        print("check the name and type again")
        return

    else:
        count = 0
        print("We found {} songs".format(len(songs)))
        for song in songs:
            count = count + 1
            print("{}). ".format(count) + song[0])

    print("which one you want to download \nplease enter the number of the song")
    y=selector_handler(len(songs))
    if (y == "quit"):
        return

    for index in y:
        songs_list=select_from_album(songs[index-1][1])

        print("there are {} songs in the album".format(len(songs_list)))

        count=0

        for song in songs_list:
            count=count+1
            print("{}). ".format(count)+song[0])

        print("which one you will like")

        y = selector_handler(len(songs_list))
        if(y=="quit"):
            return

        for index in y:
            quality=get_quality(songs_list[index-1][1])
            count=0
            if(quality_set):
                y = [-1]
            else:
                for u in quality:
                    count=count+1
                    print("{}). ".format(count)+u[0])

                print("which quality you want'")

                y = selector_handler(len(quality))
                if (y == "quit"):
                    return
            for index in y:
                x = threading.Thread(target=download_song_from_link, args=(quality[index - 1][1],))
                x.start()


def artist_search_handler():
    y = input("Type the name of the artist\n")
    artist = find_artist(y)
    print("we found {} mathces".format(len(artist)))
    count =0
    for art in artist:
        count=count+1
        print("{}). ".format(count)+art[0])

    print("which one is yours ")
    y = selector_handler(len(artist))
    y=list(y)


    songs = get_artists_songs(artist[y[0]-1][1])


    return songs






def display_help_for_select():
    print("...................................................")
    print("For selecting one option please enter the number like\n 3")
    print("...................................................")
    print("For selecting specific multiple option enter like\n 1,5,10" )
    print("...................................................")
    print("For a range of options enter like [a:b] both inclusive\n [3:9] \n [:]")
    print("...................................................")




def space_remover(sti):
    while sti[0]==" ":
        sti=sti[1:]
    while sti[-1]==" ":
        sti = sti[:-1]

    return sti

def selector_handler(max_value):
    y=input()
    if(y=="q"):
        return "quit"
    lists=y.split(",")
    options=[]
    for u in lists:
        if(len(u)!=0):

            test = space_remover(u)

            if (test[0]=="[" and test[-1]=="]"):
                rangi = test[1:-1].split(":")
                if(len(rangi)==2):
                    try:
                        if rangi[0]=="":
                            start=0
                        else :
                            start = int(rangi[0])
                        if rangi[1]=="":
                            endi=max_value
                        else :
                            endi = int(rangi[1])
                            if(int(rangi[1])>max_value):
                                endi = max_value


                        for k in range(start,endi+1):
                            options.append(k)
                    except Exception as e:
                        # raise e
                        display_help_for_select()
                else:
                    print("Not a rigth input")
                    display_help_for_select()

            else:
                try :
                    if int(test)<=max_value:
                        options.append(int(test))
                    else:
                        print("skipping {}".format(test))
                except Exception as e:
                    display_help_for_select()
                    # raise e

    return set(options)







if len(sys.argv)>1:
    songs = artist_search_handler()
else:
    songs = search_song_handler()

song_selection_hanlder(songs)

