import os, sys

print("Are you sure you want to regenerate all html files?")

while True:
    print('(y/n): ', end='')
    ans = input().lower()
    if ans == 'no' or ans == 'n':
        print('exited')
        sys.exit()
    elif ans == 'yes' or ans == 'y':
        break
    else:
        print("Invalid input")

voHeroPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'vo/vo_hero/'))
heroPagesPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'hero_pages/'))

for name in os.listdir(voHeroPath):
    if name == '.DS_Store':
        continue
    if '.DS_Store' in os.listdir(voHeroPath + '/'+name):
        os.remove(voHeroPath + '/' + name + '/.DS_Store')
        skins = os.listdir(voHeroPath + '/' + name)
        inc = len(skins)-1
    else:
        skins = os.listdir(voHeroPath + '/' + name)
        inc = len(skins)

    for skin in os.listdir(voHeroPath + '/' + name):
        skins = os.listdir(voHeroPath + '/' + name)
        if skin != '.DS_Store':
            skin_file = skin #skin_file = name of selected skin
            skins.remove(skin_file) #Remove skin selection from 'skins' array
            link_list = [] #instantiate list for alternate skin hyperlinks

            #add alternate skins to link_list
            for i in skins:
                #Convert " 'Hero' - 'Skin' " to 'Skin'
                link_list.append(i.split(' - ')[1])

            #Set 'title' variable, used for tab, main display, and alt names
            if 'Default' in skin_file:
                if 'Soldier' in name:
                    title = 'Soldier: 76'
                    pic = 'soldier76'
                    name = 'Soldier76'
                    skin_file = "Soldier76 - Default"
                elif 'Torbjorn' in name:
                    title = 'Torbjörn'
                    pic = 'torbjorn'
                    name = 'Torbjorn'
                    skin_file = "Torbjorn - Default"
                elif 'Lucio' in name:
                    title = 'Lúcio'
                    pic = 'lucio'
                    name = 'Lucio'
                    skin_file = "Lucio - Default"
                else:
                    title = name #title = default name
                    pic = title.lower()
            else:
                title = skin_file[len(name)+3:] + ' ' + name #title = name of skin + hero name
                #(ex.) skin_file = Li-Ming - Star Princess
                #          title = Star Princess Li-Ming
                pic = title.lower()

            #Write the initial lines of the html file
            header = """<!DOCTYPE html>
<html>
  <head>
    <title>{0}</title>
    <meta charset="utf-8">
    <link href="../styles/heroes.css" rel="stylesheet" type="text/css">
    <link href='http://fonts.googleapis.com/css?family=Oswald:700' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <div class="col" align="left">
      <h3><a href="../index.html" id="menu">Main Menu</a></h3>
    </div>
    <div class="col" align="center">
      <h2  id='title'>{0}</h2>
      <img src="../images/hero_images/{1}.jpg" alt="{0}"/><br>""".format(title,pic)

            text = header

            #Get old download link
            dlFound = False
            for heroFile in os.listdir(heroPagesPath):
                if heroFile != '.DS_Store':
                    if skin_file in heroFile:
                        #read heroFile
                        readFile = open(heroPagesPath + '/' + skin_file + '.html')
                        fileContent = readFile.readlines()
                        for seg in fileContent:
                            if 'mega.nz' in seg:
                                downloadURL = seg[seg.index('<a href="')+8:seg.index(" target=")]
                                dlFound = True
                        break

            #Generate html surrounding doanload link
            if dlFound is True:
                dl = """
      <a href={} target='_blank' class="link">
        <div class="download">
          <h4>Download</h4>
        </div>
      </a>
    </div>""".format(downloadURL)
            else:
                dl = """
      <a href="DOWNLOAD_LINK_HERE" target='_blank' class="link">
        <div class="download">
          <h4>Download</h4>
        </div>
      </a>
    </div>"""
                print("Missing download link for: '" + skin_file + "'")
            text += dl

            altSkinHeader = """
    <div class="col" align="right">
      <h3 id='skinParent' align='left'>"""
            text += altSkinHeader

            for i in range(0, len(skins)):
                altSkinBody = """
        <a href="{0}.html" class='skin'>{1}</a><br>""".format(skins[i],link_list[i])
                text += altSkinBody

            altSkinCloser = """
      </h3>
    </div>
    """
            text += altSkinCloser

            #Generate mp3 body
            counter = 0
            #loop through each mp3 file in skin folder
            for track in os.listdir(voHeroPath+'/{}/{}'.format(name,skin_file)):
                #ex. track = 'AnubarakCybarakBase_AI_Attack00.mp3'
                #ignore '.DS_Store'
                if track == '.DS_Store':
                  continue

                """start = track.index('_')+1 #ex. start = index of first letter after first '_',
                                           #hopefully starting at the action name
                t_name = track[start:len(track)-4] #t_name = action name without .mp3
                                                   #ex. t_name = 'AI_Attack00'
                t_name = t_name.replace('_',' ') #t_name = action name without '_'
                                                 #ex. 'AI Attack00'"""
                t_name = track
                #html audio block
                block = """
    <div class="track">
      <h4>{}</h4>
      <audio controls>
        <source src="../vo/vo_hero/{}/{}/{}" />
      </audio>
    </div>""".format(t_name,name,skin_file,track)
                #add block to file input string
                text += block
                counter += 1
            #calculate and write number of needed placeholders
            ph_count = 5 - (counter % 4)
            ph = """
    <div class="placeholder"></div>"""
            for i in range(ph_count):
                text += ph

            #Write google analytics code and closing tags
            closer ="""
    <script src='../js/jquery-1.12.2.min.js'></script>
    <script src='../js/heroScript.js'></script>
"""
            text += closer

            #Create file for hero in ../hero_pages folder named skin_file
            hero_page = open(heroPagesPath + "/{}.html".format(skin_file),"w")

            #Write text to file
            hero_page.write(text)

            #close file
            hero_page.close()
print('done')
