import os
import traceback
import json
import argparse

from pywikiapi import Site
import wikitextparser as wtp


WIKI_API = 'https://bluearchive.wiki/w/api.php'

args = None


def load_file(file, key='Name'):
    with open(file,encoding="utf8") as f:
        data = json.load(f)

    return {item[key]: item for item in data['DataList']}


def write_file(file, strategy_list):
    data = {}
    data['DataList'] = []
    for item in strategy_list.values(): 
        data['DataList'].append(item)

    f = open(os.path.join(file), 'w', encoding="utf8")
    f.write(json.dumps(data, sort_keys=False, indent=2, ensure_ascii=False))
    f.close()
    return True


def scavenge():
    global args

    page_list = []
    strategy_list = load_file(args['load_file'])

    try:
        site = Site(WIKI_API)
    except Exception as err:
        print(f'Wiki error: {err}')
        traceback.print_exc()


    for r in site.query(list='categorymembers', cmtitle='Category:Missions'):
        for page in r['categorymembers']:
            page_list.append(page)


    for page in page_list:
        text = site('parse', page=page['title'], prop='wikitext')
        print (text['parse']['title'])
        stage_code = text['parse']['title'].replace("Missions/", "")
        text_parsed = wtp.parse(text['parse']['wikitext'])
        
        for section in text_parsed.sections:
            if section.title == "Strategy":
                #print(f"Strategy found on page {text['parse']['title']}")
                wikiguide = section.contents.replace("[[Category:Missions]]", "").strip()

                if stage_code in strategy_list:
                    if strategy_list[stage_code]['Description'] == None:
                        print (f"Added guide for mission {stage_code}")
                        strategy_list[stage_code]['Description'] = wikiguide
                    elif strategy_list[stage_code]['Description'] == wikiguide:
                        print(f"Matching guides found for {stage_code}")
                        continue
                    else:
                        print (f"Conflicting strategy text added as Description_fromwiki for {stage_code}")
                        strategy_list[stage_code]['Description_fromwiki'] = wikiguide
                else:
                    print(f"New mission {stage_code} added")
                    strategy_list[stage_code] = {'Name':stage_code, 'Description':wikiguide}


    
    if len(strategy_list):
        write_file(args['write_file'], strategy_list)
        print(f"Saved {len(strategy_list)} strategies to {args['write_file']}")


def main():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('-load_file', metavar='PATH_TO_JSON_FILE', help='Existing file to load strategies from')
    parser.add_argument('-write_file', metavar='PATH_TO_JSON_FILE', help='File to write data to')
    
    args = vars(parser.parse_args())
    args['load_file'] = args['load_file'] == None and 'translation/Strategies.json' or args['load_file']
    args['write_file'] = args['write_file'] == None and 'translation/Strategies_scavenged.json' or args['write_file']
    print(args)

    try:
        scavenge()
    except:
        parser.print_help()
        traceback.print_exc()


if __name__ == '__main__':
    main()
