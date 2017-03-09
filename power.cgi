#!/usr/bin/python
#
import subprocess

def makeSwitch(num,housecode,name,state):
    info=dict()
    info['housecode']=housecode
    info['num']=num
    info['name']=name
    if (1<<(num-1)) & state[housecode]:
        info['checked']=' checked="checked"'
    else:
        info['checked']=""
    print """
<script LANGUAGE="JavaScript">
    $(document).ready(function() {                                                                                     
      $('#%(housecode)s%(num)d').change(function() {
         var cmd;
         if (this.checked) {
           cmd="on "+this.id;
         } else {
           cmd="off "+this.id;
         }                                                                                    
         x10cmd(cmd);                                                                       
      }                                                                                                                
      );                                                                                                               
    });
</script>                                                                                                                
<tr>
  <td>%(name)s</td>
  <td class="on_off">
    <input id="%(housecode)s%(num)d" type="checkbox" value="On" onclick="x10cmd('on %(housecode)s%(num)d')"%(checked)s/>
  </td>
</tr>""" % info

def getState(housecodes):
    cmds=""
    for housecode in housecodes:
        cmds=cmds+"heyu -c /var/www/x10config onstate %s\n" % housecode
    subproc = subprocess.Popen(cmds,stdout=subprocess.PIPE,shell=True)
    status = subproc.wait()
    state=dict()
    for housecode in housecodes:
        if status == 0:
            state[housecode]=int(subproc.stdout.readline()[:-1])
        else:
            state[housecode]=0
            
    return state

print("""Status: 200 OK
Content type: text/html

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>Littleton Power Switches</title>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js" type="text/javascript"></script>
  <script src="/iphone-style-checkboxes/jquery/iphone-style-checkboxes.js" type="text/javascript" charset="utf-8"></script>
  <link rel="stylesheet" href="/iphone-style-checkboxes/style.css" type="text/css" media="screen" charset="utf-8" />
  <style type="text/css">
    body {
      padding: 10px; }
    th {
      text-align: right;
      padding: 4px;
      padding-right: 15px;
      vertical-align: top; }
    .css_sized_container .iPhoneCheckContainer {
      width: 250px; }
  </style>

  <meta name="HandheldFriendly" content="true" />
  <meta name="Access-Control-Allow-Origin" value="*" />
  <meta name="viewport" content="width=device-width, height=device-height, user-scalable=no" />
<script LANGUAGE="JavaScript">


function getXMLHttpRequest() {
  if (window.XMLHttpRequest) {
    return new window.XMLHttpRequest;
  }
  else {
    try {
      return new ActiveXObject("MSXML2.XMLHTTP.3.0");
    }
    catch(ex) {
        return null;
    }
  }
}

function x10cmd(cmd) {
  var req=getXMLHttpRequest();
  if (req != null) {
    req.open("GET","X10.cgi?cmd="+cmd+"&ran="+Math.random(),true);
    req.send();
  }
  window.location.reload();
}


  
</script>
<script type="text/javascript" charset="utf-8">
    $(window).load(function() {
      $('.on_off :checkbox').iphoneStyle();
      
      var onchange_checkbox = ($('.onchange :checkbox')).iphoneStyle({
        onChange: function(elem, value) { 
          alert(value.toString());
        }
      });
      
    });

</script> 

</head>
<body>
<table style="font-size: 140%";>
""")

state=getState(("a","b"))
f=open('switches.conf','r')
for line in f.readlines():
  eval(line)
f.close

print("""
</table>
</body>
""")
