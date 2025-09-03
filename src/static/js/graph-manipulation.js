let coordinates = []; //array to hold coordinates of all nodes created

//a function that checks whether there is a node close to position of mouse
//this is to be able to move a node when a mouse is clicked on it
function close_to(x, y){
    let n = coordinates.length;
    //iterate all nodes
    for(let i=0;i<n;i++){
        let c_x = coordinates[i][0];
        let c_y = coordinates[i][1];
        //if horizontal and vertical distance is less than 10
        if(Math.abs(c_x - x) <= 10 && Math.abs(c_y-y) <= 10){
            coordinates.splice(i, 1); //delete the node from the array (because it will be moved in the future)
            return [c_x, c_y]; //and return the actual coordinates of the node 
        }
    }
    return [-1,-1]; //if nothing is found, return [-1,-1]
}


//get the diameter of node that is specified in css file
function get_node_width(graph_div){
    //create a new 'artificial' node and add a class 'node' to it
    const node = document.createElement('div'); 
    node.classList.add('node');
    graph_div.appendChild(node);
    //get the style of the node
    const nodeStyle = window.getComputedStyle(node);
    //get the width (that is also a diameter)
    const nodeWidth = parseFloat(nodeStyle.width);
    //remove the artificial node
    graph_div.removeChild(node);
    return nodeWidth;
}

//a function to check whether the position of mouse is within the graph container
function isWithinGraphDiv(graph_div, x, y){
    //get the diameter of nodes
    nodeWidth = get_node_width(graph_div);
    //get the position of the graph container
    const containerRect = graph_div.getBoundingClientRect();
    //to be within container, coordinate has to be at least a node diameter from its bounds
    //it is so that when a new node created, it doesn't go beyond the bounds
    const isWithinContainer = (
        x >= containerRect.left + nodeWidth &&
        x <= containerRect.right - nodeWidth &&
        y >= containerRect.top + nodeWidth &&
        y <= containerRect.bottom - nodeWidth
    );
    return isWithinContainer;
}

//function to add a node to a graph
function add_node(graph_div, x, y){
    //if position isn't within the graph container, node can't be added, so return false
    if(!isWithinGraphDiv(graph_div, x, y)) return false;

    //create a node - div with class node
    const node = document.createElement('div');
    node.classList.add('node');
    //add node coordinates to its id, this is for accessing it in the future
    //(for example if the node is being moved)
    node.id = x + "-" + y;
    //add the node to graph container for it to appear on the website
    graph_div.appendChild(node);
    //get the node's style -> it's width/diameter
    const nodeStyle = window.getComputedStyle(node);
    const nodeWidth = parseFloat(nodeStyle.width);
    //calculate top and left coordinates of node by substracting half diameter from centre
    node.style.left = x - nodeWidth/2 +'px';
    node.style.top = y - nodeWidth/2 +'px';
    //add coordinates of created node to the coordinates array to keep track of the nodes
    coordinates.push([parseFloat(x), parseFloat(y)]);
    //return true because the node was created
    return true;
}

//function to generate random nodes
function generate_cities(div, n){
    clear_graph(div);//clear all nodes first
    nodeWidth = get_node_width(div);//get diameter of the node
    //get and calculate the bounds of graph container
    //nodes should be at least diameter from the actual bounds so that nodes don't touch the bound
    const containerRect = div.getBoundingClientRect();
    const left = containerRect.left + nodeWidth;
    const right = containerRect.right - nodeWidth;
    const top = containerRect.top + nodeWidth;
    const bottom = containerRect.bottom - nodeWidth;

    generated = 0;
    while (generated<n){ //lop while didn't generate n nodes
        //create a random coordinate within the container bounds
        let x = Math.floor(Math.random() * (right - left + 1)) + left; 
        let y = Math.floor(Math.random() * (top - bottom + 1)) + bottom;
        //if a node can be added (add_node returns true), that increase the count of generated
        if(add_node(div, x, y)) generated++; 
    }
}

//event listener for any of users mouse moves/clicks, etc
document.addEventListener('DOMContentLoaded', function(){
    //graph_div is a graph container, that we access by id
    const graph_div = document.getElementById("graph-div");
    //initialise values that we use for graph manipulation
    let selected_node = null;
    let created_node = 0;

    //if users moves mouse down (clicks), it can mean three things:
    //user wants to move a node (if mouse position is close to an existing node)
    //user wants to delete a node (if first applies and it's a right click/ctrl is pressed)
    //if neither of 2 above, user wants to create a new node, but we only add it to display when mouse is moved up
    graph_div.addEventListener('mousedown', function(event){
        //get the coordinates of user's mouse
        const x = event.clientX;
        const y = event.clientY;
        //proceed if and only if mouse position is within the container bounds that allow nodes inside
        if(isWithinGraphDiv(graph_div, x, y)){
            //graph_locked is true if visualisation is on (se display-output.js for reference)
            if(graph_locked){ //if visualisation is on, user can't do any changes to the display
                //user needs to clear the paths created in the visualisation to be able to edit the display
                alert("clear the paths to edit the graph");
                return;
            }
            //event.button == 2 is if user right clicked
            //on mac, there is no right click, so we have to add an option with a ctrl key
            const right_click = (event.button == 2) || (event.ctrlKey); 

            let close_to_coordinate = close_to(x, y); 
            //if there is a node that the coordinate is close to, user either wants to move it or delete it
            if (close_to_coordinate[0]!=-1){
                //create an id of the node the mouse is close to
                let id = close_to_coordinate[0]+"-"+close_to_coordinate[1];
                //here we assume that user wants to move the node, and set the selected node to the close node
                selected_node = document.getElementById(id);
                selected_node.style.cursor = 'grabbing';//change the style of the node to grabbing 
                //however, if the user right clicks, they want to delete the node, and not move it
                if(right_click){
                    event.preventDefault();//this is just so that context menu doesn't show up as default when right clicking
                    //delete the node from the container
                    graph_div.removeChild(selected_node);
                    //because we used close_to function before, we don't need to delete the node from coordinates array 
                    //    as it was already removed from there
                    selected_node = null; //set selected_node back to null as we've deleted the node that was selected
                }
            }
            else if (!right_click) created_node = 1; //if there is no close node and it's not right click, a node is to be created
            //but instead of creating it now, we save a state of creating it, and add to visual display when mouse is realeased
        }
    })
    //if mouse is moved, it only has an effect on graph when a node is selected (so user moves that selected node)
    graph_div.addEventListener('mousemove', function(event){
        //get the coordinates of the mouse
        const x = event.clientX;
        const y = event.clientY;
        //check whether position is within the bounds (to prevent nodes being moved outside the container) and if node is selected
        if(isWithinGraphDiv(graph_div, x, y) && selected_node){
            //change the node position to the position of the mouse - radius
            nodeWidth = get_node_width(graph_div);//get node width/diameter
            selected_node.style.left = x-nodeWidth/2+'px';
            selected_node.style.top = y-nodeWidth/2+'px';
            //update the id 
            selected_node.id = x+"-"+y;
            //note that we don't edit anything in coordinates array here
            //this is because we deleted the node from the array when it was selected and we will add it back in when mouse is released
        }
    })
    //if mouse is released it can mean 2 things:
    //user moved the selected node to its final position (if selected_node is not null)
    //user created a node and it is to be added to display when mouse is realesed (if created_node is true)
    graph_div.addEventListener('mouseup', function(event){
        if (selected_node){//if node is selected, this node was being moved and now has to be added to coordinates array
            //get the coordinates of the node from its id (id is in the form 'x-y')
            //note that we don't use the position of the mouse here, as it could be moved outside of bounds and then released
            const x = selected_node.id.split("-")[0];
            const y = selected_node.id.split("-")[1];
            coordinates.push([parseFloat(x), parseFloat(y)]); //add coordinates to coordinates array to keep it in sync
            selected_node.style.cursor = 'grab'; //change cursor back to grab
            selected_node = null;//node is no longer selected, so reset selected_node to null
        }
        else if (created_node){//if node was created, it has to be added to the display
            created_node = 0; //reset created_node back to 0
            //get the coordinates of the mouse
            const x = event.clientX;
            const y = event.clientY;
            if(isWithinGraphDiv(graph_div, x, y)){ //if coordinates are within the bounds, add the node
                add_node(graph_div, x, y);
            }
        }
    });
    //this is to prevent contexmenu from showing up when user right clicks
    graph_div.addEventListener("contextmenu", function (event) {
        event.preventDefault();
    });
    //if generate button is clicked, generate a graph
    document.getElementById("btn-generate").addEventListener("click", function () {
        //graph_locked is true if visualisation is on (se display-output.js for reference)
        //if(graph_locked){ //if visualisation is on, user can't do any changes to the display
            //user needs to clear the paths created in the visualisation to be able to edit the display
            //alert("clear the paths to edit the graph");
            //return;
        //}
        //get the value of number of cities input
        const numberOfCities = parseInt(document.getElementById("cities-input").value);
        //if numberOfCities is a positive integer, generate cities
        if (!isNaN(numberOfCities) && Number.isInteger(numberOfCities) && numberOfCities > 0) {
            generate_cities(graph_div, numberOfCities);
        } else { //else output an alert
            alert("Please enter a valid positive integer for the number of cities.");
        }
    });

})