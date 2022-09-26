const { contextBridge, ipcRenderer } = require('electron');
window.addEventListener('DOMContentLoaded', () => {
  contextBridge.exposeInMainWorld(
    "api", {
        send: (channel, data) => {
            // whitelist channels
            // document.getElementById('selectedItem').value = `You selected: ${data}`
            let validChannels = [
              "tomain",
              "load_project_to_main",
              "load_xrd_to_main",
              "load_strain_to_main",
              "load_dw_to_main",
              "change_title",
              "closeElectronWindow",
              "save_project_to_main",
              "change_theme_color"
            ];
            if (validChannels.includes(channel)) {
                ipcRenderer.send(channel, data);
            }
        },
        receive: (channel, func) => {
          let validChannels = [
            "NewProject",
            "SaveProject",
            "SaveCurrentProject",
            "fromMain",
            "load_project_from_main",
            "load_xrd_from_main",
            "load_strain_from_main",
            "load_dw_from_main",
            "change_title",
            "SaveFitData",
            "LogFile",
            "OpenOptionsRadmax",
            "AboutRadmax"
          ];
          if (validChannels.includes(channel)) {
              // Deliberately strip event as it includes `sender` 
              ipcRenderer.on(channel, (event, ...args) => func(...args));
          }
        }
      }
    );
})