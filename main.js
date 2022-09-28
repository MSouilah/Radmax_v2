// Modules to control application life and create native browser window
const {app, globalShortcut, BrowserWindow, Menu} = require('electron');
const path = require('path');
const { dialog } = require('electron');
var fs = require('fs');
const ipc = require('electron').ipcMain;

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;
function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1200,
    // fullscreen: true,
    icon: __dirname + "/web/img/icone_radmax_2.png",
    webPreferences: {
      nodeIntegration: false,
      preload: path.join(__dirname, 'preload.js')
    }
  })
  console.log("Yoda")
  const menu = Menu.buildFromTemplate(exampleMenuTemplate());
  Menu.setApplicationMenu(menu);

  // and load the index.html of the app.
  mainWindow.loadURL('http://localhost:8000/index.html');

  // Open the DevTools.
  mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
  })

  mainWindow.on('close', function (event) {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    let choice = dialog.showMessageBoxSync(this,
        {
        type: 'question',
        buttons: ['Yes', 'No'],
        title: 'Confirm',
        message: 'Are you sure you want to quit?'
    });
    if (choice == 1) {
        event.preventDefault();
      }else{
        mainWindow.destroy();
      }
  })
}

if (process.platform === 'win32') {
  // Redirect node's console to use our own implementations, since node can not
  // handle console output when running as GUI program.
  const origLog = console.log
  var consoleLog = function (...args) {
    origLog.call(console, ...args);
    return process.log(util.format(...args) + '\n')
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
// app.on('ready', createWindow)

app.whenReady().then(() => {
  createWindow();
})

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    // OnExitApp();
    if (process.platform !== 'darwin' && app.listeners('window-all-closed').length === 1 && !option.interactive){
        mainWindow.close();
        app.quit();
    }
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow()
})


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
var OnExitApp = function(event) {
  let choice = dialog.showMessageBoxSync(mainWindow,
    {
      type: 'question',
      buttons: ['Yes', 'No'],
      title: 'Confirm',
      message: 'Are you sure you want to quit?'
    });
  if (choice == 1) {
    event.preventDefault();
  }else{
    mainWindow.destroy();
  }
};

var showOpen = function(event) {
    dialog.showOpenDialog(
      { properties: ['openFile'], title : "Open project file", filters: [{ name: 'ini', extensions: ['ini'] }, { name: 'Tous les fichiers', extensions: ['*'] }]}
    ).then
    (
        result => {
            if (!result.canceled)
            {
              mainWindow.webContents.send('load_project_from_main', result.filePaths)
            }
        }
    ).catch(err => {
      console.log(err)
  });
};

var showOpenXRD = function(event) {
  dialog.showOpenDialog(
    { properties: ['openFile'], title : "Open XRD data", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]}
  ).then
  (
      result => {
          if (!result.canceled)
          {
            mainWindow.webContents.send('load_xrd_from_main', result.filePaths)
          }
      }
  ).catch(err => {
    console.log(err)
  });
};

var showOpenStrain = function(event) {
  dialog.showOpenDialog(
    { properties: ['openFile'], title : "Open Strain data", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]}
  ).then
  (
      result => {
          if (!result.canceled)
          {
            mainWindow.webContents.send('load_strain_from_main', result.filePaths)
          }
      }
  ).catch(err => {
    console.log(err)
  });
};

var showOpenDW = function(event) {
  dialog.showOpenDialog(
    { properties: ['openFile'], title : "Open DW data", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]}
  ).then
  (
      result => {
          if (!result.canceled)
          {
            mainWindow.webContents.send('load_dw_from_main', result.filePaths)
          }
      }
  ).catch(err => {
    console.log(err)
  });
};

var showSave = function() {
	dialog.showSaveDialog(
    { properties: ['openFile'], title : "Save project",  filters: [{ name: 'ini', extensions: ['ini'] }]}
  ).then
  (
      result => {
          if (!result.canceled)
          {
            mainWindow.webContents.send('SaveProject', result.filePath)
          }
      }
  ).catch(err => {
    console.log(err)
  });
};

ipc.on('closeElectronWindow', function (event) {
  OnExitApp();
})

ipc.on('tomain', function (event) {
  var fileOpen = dialog.showOpenDialog(
    { properties: ['openFile'], title : "Open project", filters: [{ name: 'ini', extensions: ['ini'] }, { name: 'Tous les fichiers', extensions: ['*'] }]})
    fileOpen.then(
      result => event.sender.send('fromMain', result.filePaths)
    );
})

ipc.on('load_project_to_main', function (event) {
  var fileOpen = dialog.showOpenDialog(
    { properties: ['openFile'], title : "Load project file", filters: [{ name: 'ini', extensions: ['ini'] }]})
    fileOpen.then(
      result => event.sender.send('load_project_from_main', result.filePaths)
    );
})

ipc.on('load_xrd_to_main', function (event) {
  var fileOpen = dialog.showOpenDialog(
    { properties: ['openFile'], title : "Load XRD file", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]})
    fileOpen.then(
      result => event.sender.send('load_xrd_from_main', result.filePaths)
    );
})

ipc.on('load_strain_to_main', function (event) {
  var fileOpen = dialog.showOpenDialog(
    { properties: ['openFile'], title : "Load Strain file", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]})
    fileOpen.then(
      result => event.sender.send('load_strain_from_main', result.filePaths)
    );
})

ipc.on('load_dw_to_main', function (event) {
  var fileOpen = dialog.showOpenDialog(
    { properties: ['openFile'], title : "Load DW file", filters: [{ name: 'Tous les fichiers', extensions: ['*'] }]})
    fileOpen.then(
      result => event.sender.send('load_dw_from_main', result.filePaths)
    );
})

ipc.on('change_title', function (event, arg) {
  let name = require('./package.json').name;
  let windowTitle = name + " - " + arg;
  mainWindow.setTitle(windowTitle)
})

ipc.on('save_project_to_main', function (event, arg) {
  showSave();
})

ipc.on('change_theme_color', function (event, arg) {

})

const isMac = process.platform === 'darwin';

const exampleMenuTemplate = () => [
	{
		label: "File",
    submenu: [
      {
        label: "New project",
        click: function() { 
          mainWindow.webContents.send('NewProject')
        },
        accelerator: 'Ctrl+N'
      },
      {
        label: "Load project",
        click: function() {
          showOpen();
        },
        accelerator: 'Ctrl+O'
      },
      {type: "separator"},
      {
        label: "Import XRD",
        click: function() {
          showOpenXRD();
        },
        accelerator: 'Alt+O'
      },
      {
        label: "Import Strain",
        click: function() { 
          showOpenStrain();
        }
      },
      {
        label: "Import DW",
        click: function() { 
          showOpenDW();
        }
      },
      {type: "separator"},
      {
        label: "Export Strain, DW, XRD fit",
        click: function() { 
          mainWindow.webContents.send('SaveFitData');
        }
      },
      {type: "separator"},
      {
        label: "Save AS",
        click: function() { showSave();},
        accelerator: 'Ctrl+Shift+S'
      },
      {
        label: "Save",
        click: function() {
          mainWindow.webContents.send('SaveCurrentProject');
        },
        accelerator: 'Ctrl+S'
      },
	    {type: "separator"},
	    {
        label: "Exit",
        click: function() { 
          OnExitApp();
        },
        // click: () => app.quit(),
        accelerator: 'Alt+X'
      },
    ]
	},
  {
    label: "Options",
    submenu: [
      {
        label: "Database and Sounds",
        click: (item) => {
          mainWindow.webContents.send('OpenOptionsRadmax');
        }
      },
      {
        label: "Log file",
        click: (item) => {
          mainWindow.webContents.send('LogFile');
        }
      }
    ]
  },
  {
    label: 'About',
    role: 'help',
    submenu: [
      {
        label: 'About RaDMaX',
        click: (item) => {
          mainWindow.webContents.send('AboutRadmax');
        }
      },
      {
        label: 'Toggle Developer Tools',
        click(item, focusedWindow) {
          if (focusedWindow) focusedWindow.webContents.toggleDevTools();
        }
      }
    ]
  }
];

