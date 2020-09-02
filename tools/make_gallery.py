#! /usr/bin/env python3


import glob


HTML_HEADER = """
<html>
<style>
  img {
      border-radius: 3px;
      margin-bottom: 4px;
      width: 300px;
  }
  div.thumb {
      color: #888;
      display: inline-block;
      font: 10px sans-serif;
      background-color: #efefef;
      border-radius: 3px;
      border: solid 1px #ddd;
      margin: 5px;
      padding: 5px;
      cursor: hand;
  }
  div.thumb:hover {
      color: maroon;
      border-color: skyblue;
      font-weight: bold;
  }
  div.thumbframe {
      border-right: solid 1px #cce;
      float: left;
      max-height: 100%;
      overflow-x: scroll;
      width: 340px;
  }
  #full-size {
      border: none;
      float: right";
      height: 100%;
      width: 1000px;
  }
</style>
</html>
"""

def main():
    print(HTML_HEADER)
    print('<div class="thumbframe">')
    for imfile in sorted(glob.iglob('**/*', recursive=True)):
        if not imfile.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            continue
        print('  <div class="thumb">')
        print('  <img src="{0}" '
              'onclick="document.getElementById(\'full-size\').setAttribute(\'src\', \'{0}\');"/>'.format(imfile))
        print('  <div style="text-align: center">{}</div>'.format(imfile))
        print('  </div>')
    print('</div>')
    print('<img id="full-size"/>')
    print('</html>')

if __name__ == '__main__':
    main()
