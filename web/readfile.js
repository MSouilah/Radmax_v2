var fs = require('fs');

var filepath = '../modules/Radmax.ini';
let theme = "";
const DARK_THEME_PATH = "/css/Bootswatch5.1.2_cyborg.min.css";
const SANDSTONE_THEME_PATH = "/css/Bootswatch5.1.2_sandstone.min.css";
const DARK_STYLE_LINK = document.getElementById("dark-theme-style");

fs.readFile(filepath, 'utf-8', (err, data) => {
  if(err) throw err;
  const arr = data.toString().replace(/\r\n/g,'\n').split('\n');
  theme_index = arr.indexOf("[Theme]");
  tmp = arr[theme_index + 1].split('=');
  theme = tmp[1].replace(/ /g,'');
  if(theme == 0){
        DARK_STYLE_LINK.setAttribute("href", "https://cdn.jsdelivr.net/npm/bootstrap@5.1.2/dist/css/bootstrap.min.css");
    }
    else if (theme == 1){
        DARK_STYLE_LINK.setAttribute("href", DARK_THEME_PATH);
    }else{
        DARK_STYLE_LINK.setAttribute("href", SANDSTONE_THEME_PATH);
    }
});