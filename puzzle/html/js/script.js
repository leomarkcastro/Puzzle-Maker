//  self    ->  referes to the static html
//  root    ->  refers to the live window

//  stdout.println("selected file: "); 
//  view.gprint("Hello boys");

var root = view.root;

var DOM = {
    tab : {
        play : root.select(".play_tab"),
        print : root.select(".print_tab")
    },
    tab_button : {
        play : root.select("#play"),
        print : root.select("#print")
    },
    play_tab : {
        pickList : root.select(".pickGame"),
        paramList : root.select(".paramGame"),
    },
    print_tab : {
        printSettingsButton : root.select(".printSettings .button"), //plus the params
        printChoices : root.select(".printChoices"),
        queueList : root.select(".queueList"),
    },
    overlay: {
        mainOverlay : root.select(".overlay"),

        overlayNotif: root.select(".overlay_notif"),
        overlayNotif_box: root.select(".notif_box"),

        overlayLoad: root.select(".overlay_loading"),
        overlayLoad_box: root.select(".loading_box"),
        overlayLoad_title: root.select(".lb_title"),
        overlayLoad_detail: root.select(".lb_detail"),
        overlayLoad_bar: root.select(".loadingBar"),

    }
}
var PlayInputWatch = {}

var PrintQueue = {
    index : 0
}
var PrintQueueList = []


/* UTILITY FUNCTIONS */

function print(msg){
    view.gprint(msg);
}

function move(array, from, to) {
    array.splice(to, 0, array.splice(from, 1)[0]);
};



/* FUNCTIONS TO MANAGE THE VIEW */

function changeTab(mode){
    //Reset methods
    DOM.tab.play.attributes.addClass("hide")
    DOM.tab.print.attributes.addClass("hide")
    DOM.tab_button.play.attributes.removeClass("selected")
    DOM.tab_button.print.attributes.removeClass("selected")

    
    DOM.tab[mode].attributes.removeClass("hide")
    DOM.tab_button[mode].attributes.addClass("selected")
}

function buttonsAction_Play(string){
    DOM.play_tab.paramList.attributes.removeClass("flex0");
    buttonsAction_Play_LoadBoard(string)
}

function buttonsAction_Play_LoadBoard(string){
    DOM.play_tab.paramList.html =  
    `<div class="param_play">
        <div class="button">PLAY GAME</div>
        <div class="buttonContainer">
            <div class="buttonEasy">Easy</div>
            <div class="buttonMedium">Medium</div>
            <div class="buttonHard">Hard</div>
        </div>
    </div>`
    // There's this function that will get a dictionary to process
    let sample = view.loadPlayData(string, "Easy");

    function createParameters(label, params, id){
        let html = ''
        let opt = ''
        switch (params[0]){

            case ('number'):

                html = String.printf(`<div class="param_set" id="%s">
                        <label class="param_label">%s</label>
                        <input type="integer" step="1" value="%d" min="%d" max="%d"/>
                    </div>`, id, label, params[1], params[2], params[3]);

                break;
            
            case ('choice'):
                opt = ``
                for (let item in params[2]){
                    opt += String.printf('<option>%s</option>',item)
                }

                html = String.printf(
                    `<div class="param_set" id="%s">
                        <label class="param_label">%s</label>
                        <select type="dropdown">
                            %s
                        </select>
                    </div>`, id, label, opt);
                
                break;

                case ('file'):
    
                    html = String.printf(
                        `<div class="param_set" id="%s">
                            <label class="param_label">%s</label>
                            <button>Pick File</button>
                        </div>`, id, label);
                    
                    break;

        }
        
        
        DOM.play_tab.paramList.html =  html + DOM.play_tab.paramList.html;
        PlayInputWatch[label] = [id, params[1]];
    }

    //The parameter builders
    PlayInputWatch = {}
    let id=0;
    for (let param in sample){
        createParameters(param, sample[param], String.printf(`playParam%d`,id));
        id += 1
    }
    DOM.play_tab.paramList.html =  "<h3>Parameters: " + string + "</h3>" + DOM.play_tab.paramList.html;
    
}

function buttonsAction_Play_LoadPreset(mode){

    let sample = view.loadPlayPreset(mode)

    function changeParameters(label, params){

        let data = PlayInputWatch[label]
        
        let curDat = root.select("#"+data[0])

        switch (params[0]){
            
            case ('number'):

                curDat.select("input").value = params[1]

                break;
            
            case ('choice'):

                curDat.select("select").value = params[1]

                break;

            case ('file'):

                break;

        }

    }

    for (let label in sample){
        changeParameters(label, sample[label]);
    }
}

function buttonsAction_Play_PlayGame(){
    let retVal = {}

    for (let keys in PlayInputWatch){
        try{
            retVal[keys] = root.select("#"+PlayInputWatch[keys][0]+ " input").value;
        }
        catch(e){
            retVal[keys] = root.select("#"+PlayInputWatch[keys][0]+ " select").value;
        }

    }

    view.loadPlayStartGame(retVal);
}

function buttonsAction_Print_CreateQueue(title){

    // There's this function that will get a dictionary to process
    let sample = view.loadPlayData(title, "Easy");

    function createParameters(label, params, id){
        let html = ''
        let opt = ''
        switch (params[0]){

            case ('number'):

                html = String.printf(`<div class="param_set" id="%s">
                        <label class="param_label">%s</label>
                        <input type="integer" step="1" value="%d" min="%d" max="%d"/>
                    </div>`, id, label, params[1], params[2], params[3]);

                break;
            
            case ('choice'):
                opt = ``
                for (let item in params[2]){
                    opt += String.printf('<option>%s</option>',item)
                }

                html = String.printf(
                    `<div class="param_set" id="%s">
                        <label class="param_label">%s</label>
                        <select type="dropdown">
                            %s
                        </select>
                    </div>`, id, label, opt);
                
                break;

                case ('file'):
    
                    html = String.printf(
                        `<div class="param_set" id="%s">
                            <label class="param_label">%s</label>
                            <button>Pick File</button>
                        </div>`, id, label);
                    
                    break;

        }
        
        
        return html
    }

    //The parameter builders
    let data = {}
    let rootID = PrintQueue.index;
    let id=0;
    let pack = `<div class="queueItem"><h5>`+title+`</h5>`

    data["Title"] = title;
    for (let param in sample){
        pack = pack + createParameters(
            param, 
            sample[param], 
            String.printf(`playParam%d_%d`,rootID ,id)
            );
        data[param] = String.printf(`playParam%d_%d`,rootID ,id);
        id += 1;
    }
    pack += 
    `<div class="buttonContainer">
        <p class="buttonX">Remove</p>
        <p class="buttonUP">Move Up</p>
        <p class="buttonDOWN">Move Down</p>
    </div></div>`;
    PrintQueueList.push(data)


    PrintQueue.index += 1;
    DOM.print_tab.queueList.html += pack;
}

function buttonsAction_Rearrange(element, direction){
    switch (direction){
        case (-1):
            move(PrintQueueList, element.index, element.index-1);
            break;
        case (2):
            move(PrintQueueList, element.index, element.index+1);
            break;
    }
    element.parent.insert(element, element.index+direction)
}

function buttonsAction_Remove(element){
    let index = element.index;
    if (index > -1) {
        PrintQueueList.splice(index, 1);
    }
    element.remove();
}

function overlay_ShowNotification(title, message){

    DOM.overlay.mainOverlay.attributes.removeClass("height0");
    DOM.overlay.mainOverlay.style["height"] = "100vh";

    DOM.overlay.overlayNotif.attributes.addClass("hide");
    DOM.overlay.overlayLoad.attributes.addClass("hide");

    DOM.overlay.overlayNotif.attributes.removeClass("hide");
    
    DOM.overlay.overlayNotif_box.html = 
    String.printf(`<h3>%s</h3>
    <p>%s</p><p class="prompt">Click anywhere to dismiss...</p>`, title, message);

}

/* LISTENERS OF THE DOM */

DOM.tab_button.play.on("click", function(){changeTab("play")});

DOM.tab_button.print.on("click", function(){changeTab("print")});

DOM.play_tab.pickList.on("click", function(e){
    let curPoint = e.target;
    let attr = curPoint.attributes
    if (attr.hasClass("buttons")){
        buttonsAction_Play(curPoint.text);
    }
    
});

DOM.play_tab.paramList.on("click", function(e){
    let curPoint = e.target;
    if (curPoint.attributes.hasClass("button")){
        buttonsAction_Play_PlayGame();
    }
    else if (curPoint.parent.attributes.hasClass("buttonContainer")){
        buttonsAction_Play_LoadPreset(curPoint.text);
    }
});

DOM.print_tab.printChoices.on("click", function(e){
    let curPoint = e.target;
    if (curPoint.attributes.hasClass("buttons")){
        buttonsAction_Print_CreateQueue(curPoint.text);
    }
});

DOM.print_tab.queueList.on("click", function(e){
    let curPoint = e.target;
    if (curPoint.attributes.hasClass("buttonX")){
        buttonsAction_Remove(curPoint.parent.parent);
    }
    else if (curPoint.attributes.hasClass("buttonUP")){
        let elementPlace = curPoint.parent.parent;
        buttonsAction_Rearrange(elementPlace, -1);
    }
    else if (curPoint.attributes.hasClass("buttonDOWN")){
        let elementPlace = curPoint.parent.parent;
        buttonsAction_Rearrange(elementPlace, 2);
    }
    
});

DOM.overlay.mainOverlay.on("click", function(e){
    
    DOM.overlay.overlayLoad.attributes.addClass("hide");
    DOM.overlay.overlayNotif.attributes.addClass("hide");
    DOM.overlay.mainOverlay.attributes.addClass("height0");
    DOM.overlay.mainOverlay.style["height"] = "0";
    
})
