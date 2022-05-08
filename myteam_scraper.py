import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def get_player_links(num_pages):
    
    ret_list = []
    for p in range(num_pages):

        # get page
        page = BeautifulSoup(requests.get('http://mtdb.com/22?page=' + str(p+1) + '&sortedBy=overall&sortOrder=Descending&').text)
        
        # loop over page and remove unneeded tows
        for i in str(page).split('</tr>'):
            for j in i.split('</td>'):
                if 'href="/22/players' in j:
                    if len(j.strip()) < 200:

                        # format link and add to list
                        link = j.strip().split('\n')[2]
                        link = link[9:]
                        link = link[:link.index('>')-1]
                        ret_list.append('http://mtdb.com' + link)
    return ret_list

playerLink = get_player_links(86) # currrently 86 pages of players
# get top ten to test with
ten = playerLink[:10]

cols = ['Player', 'PlayerID', 'Weight (lbs.)', 'Height', 'Height (In.)', 'Overall', # general
'Mid-Range Shot', 'Shot IQ','Three-Point Shot','Free Throw','Offensive Consistency', # shooting
'Close Shot','Driving Layup','Standing Dunk','Driving Dunk','Draw Foul','Post Moves','Post Hook','Post Fadeaway', # inside scoring
'Ball Handle','Pass Accuracy','Pass IQ', # playmaking
'Speed','Speed With Ball', 'Acceleration','Vertical','Strength','Stamina','Hustle', # athleticsm
'Help Defensive IQ','Lateral Quickness','Pass Perception','Block','Perimeter Defense','Defensive Consistency','Interior Defense','Steal', # defense
'Offensive Rebound', 'Defensive Rebound', # rebounding
'Total Attributes']

top500 = playerLink[:500]

masterList = []
for link in top500:
    
    page = BeautifulSoup(requests.get(link).text)
    dataList = []
    
    # get player name from link
    nameID = link[link.index('players/')+8:]
    name = nameID[:-2]
    name = re.sub('-', ' ', name).strip()
    dataList.append(name)
    dataList.append(nameID)
    attr = []
    
    for i in str(page).split('</ul>'):
        
        for j in i.split('\n'):
            
            # get height and weight
            if 'lbs /' in j:
                weight = j.split('/')[7].split()[0]
                height = j.split('/')[8].strip()
                ft = int(height[0])
                inch = int(height[2])
                heightInch = 12*ft+inch
                dataList.append(weight)
                dataList.append(height)
                dataList.append(heightInch)
            
            # get player overall
            if '"statNum playerONum" style="display: block;"' in j:
                overall = j[j.index('block;">')+8:]
                
                dataList.append(int(overall[:overall.index('<')]))
            
            # get all data vals
            if 'statNum' in j:
                if '<li>' in j:

                    data = j[j.index('style="">')+9:]
                    data = data[:data.index('<')]
                    dataList.append(int(data))
                    attr.append(int(data))
     
    # add valid rows to list
    if len(dataList) == 72:
        
        totalAttr = sum(attr[:33])
        row = dataList[:39]
        row.append(totalAttr)
        masterList.append(row)
        
attributes = pd.DataFrame(masterList, columns = cols)

# map gem type
gems = {99:'Dark Matter',
        98:'Galaxy Opal', 97:'Galaxy Opal',
        96:'Pink Diamond', 95:'Pink Diamond',
        94:'Diamond', 93:'Diamond', 92:'Diamond',
        91:'Amethyst', 90:'Amethyst',
        89:'Ruby', 88:'Ruby', 87:'Ruby',
        86:'Sapphire', 85:'Sapphire', 83:'Sapphire',
        84:'Emerald', 82:'Emerald', 81:'Emerald', 80:'Emerald',
        79:'Gold', 78:'Gold', 77:'Gold', 76:'Gold', 75:'Gold', 74:'Gold', 73:'Gold', 72:'Gold',
        71:'Gold', 70:'Gold', 69:'Gold', 68:'Gold', 67:'Gold', 66:'Gold', 65:'Gold', 64:'Gold'}

attributes['Gem Type'] = attributes['Overall'].map(gems)

badgeDict = {'putbackboss':0, 'dropstepper':0, 'backdownpunisher':0, 'fearlessfinisher':0, 'hookspecialist':0, 'posterizer':0,
'riseup':0, 'limitlesstakeoff':0, 'fasttwitch':0, 'acrobat':0, 'lobcityfinisher':0, 'protouch':0, 'slithery':0, 'unstrippable':0,
'mouseinthehouse':0, 'graceunderpressure':0, 'teardropper':0, 'giantslayer':0, 
'clutchshooter':0, 'hotzonehunter':0, 'fadeace':0, 'rhythmshooter':0, 'setshooter':0, 'cornerspecialist':0, 'difficultshots':0,
'catchandshoot':0, 'deadeye':0, 'greenmachine':0, 'mismatch':0, 'luckynumber7':0, 'blinders':0, 'circusthree':0, 'limitlessspotup':0,
'sniper':0, 'volumeshooter':0, 'slipperyoffball':0, 'chef':0, 'stopandpop':0, 
'postspintechnician':0,'downhill':0,'quickfirststep':0,'bailout':0,'dreamshake':0,'neddlethreader':0,'spacecreator':0,'unpluckable':0,'gluehands':0,
'bulletpasser':0,'postplaymaker':0,'anklebreaker':0,'dimer':0,'breakstarter':0,'floorgeneral':0,'handlesfordays':0,
'tighthandles':0,'hyperdrive':0,'ballandchain':0, 'stopandgo':0,'specialdelivery':0,'triplethreatjuke':0, 'rimprotector':0,'box':0,
'clamps':0,'interceptor':0,'intimidator':0,'pogostick':0,'postmovelockdown':0,'reboundchaser':0,'worm':0,'brickwall':0,
'chasedownartist':0,'offballpest':0,'tirelessdefender':0,'defensiveleader':0,'menace':0,
'hustler':0,'pickdodger':0,'pickpocket':0,'anklebrace':0,'ballstripper':0}

badgeDF = pd.DataFrame(badgeDict, index=[0])
len(badgeDict)

masterList = []
for link in top500:
    badgeList = []
    
    # get player name from link
    nameID = link[link.index('players/')+8:]
    name = nameID[:-2]
    name = re.sub('-', ' ', name).strip()
    
    for i in str(BeautifulSoup(requests.get(link + '/personality-badges').text)).split('</span>'):

        if 'img src' in i:
            for j in i.split('>'):

                if 'img src' in j:
                    if '22/badges' in j:

                        badge = j[j.index('badges/')+7:-6].split('_')
                        badge = badge[0].strip() + ' ' + badge[1].strip()
                        badgeList.append(badge.strip())
              
    badgeDict = {'putbackboss':0, 'dropstepper':0, 'backdownpunisher':0, 'fearlessfinisher':0, 'hookspecialist':0, 'posterizer':0,
                'riseup':0, 'limitlesstakeoff':0, 'fasttwitch':0, 'acrobat':0, 'lobcityfinisher':0, 'protouch':0, 'slithery':0, 'unstrippable':0,
                'mouseinthehouse':0, 'graceunderpressure':0, 'teardropper':0, 'giantslayer':0, 
                'clutchshooter':0, 'hotzonehunter':0, 'fadeace':0, 'rhythmshooter':0, 'setshooter':0, 'cornerspecialist':0, 'difficultshots':0,
                'catchandshoot':0, 'deadeye':0, 'greenmachine':0, 'mismatch':0, 'luckynumber7':0, 'blinders':0, 'circusthree':0, 'limitlessspotup':0,
                'sniper':0, 'volumeshooter':0, 'slipperyoffball':0, 'chef':0, 'stopandpop':0, 
                'postspintechnician':0,'downhill':0,'quickfirststep':0,'bailout':0,'dreamshake':0,'neddlethreader':0,'spacecreator':0,'unpluckable':0,'gluehands':0,
                'bulletpasser':0,'postplaymaker':0,'anklebreaker':0,'dimer':0,'breakstarter':0,'floorgeneral':0,'handlesfordays':0,
                'tighthandles':0,'hyperdrive':0,'ballandchain':0, 'stopandgo':0,'specialdelivery':0,'triplethreatjuke':0, 'rimprotector':0,'box':0,
                'clamps':0,'interceptor':0,'intimidator':0,'pogostick':0,'postmovelockdown':0,'reboundchaser':0,'worm':0,'brickwall':0,
                'chasedownartist':0,'offballpest':0,'tirelessdefender':0,'defensiveleader':0,'menace':0,
                'hustler':0,'pickdodger':0,'pickpocket':0,'anklebrace':0,'ballstripper':0}
    
    for bad in badgeList:
        if bad != 'null':
            if '-' not in bad:
                spl = bad.split(' ')
                
                if spl[1] == 'bronze':
                    badgeDict[spl[0]] = 1
                elif spl[1] == 'silver':
                    badgeDict[spl[0]] = 2
                elif spl[1] == 'gold':
                    badgeDict[spl[0]] = 3
                elif spl[1] == 'amethyst':
                    badgeDict[spl[0]] = 4   
    row = []
    row.append(name)
    row.append(nameID)
    
    for i in list(badgeDict.values()):
        row.append(i)
    
    masterList.append(row)
    
cols = []
cols.append("Player")
cols.append("PlayerID")
for i in list(badgeDict.keys()):
    cols.append(i)
    
    
badges = pd.DataFrame(masterList, columns = cols)

nba2kDF = attributes.merge(badges, on='PlayerID')

file = open('myteam_players.csv', 'w')
file.write(nba2kDF.to_csv())
file.close()












