class path{
	constructor(position,distance,previous)
	{
		this.position = position;
		this.distance = distance;
		this.previous = previous
	}

}


class deque{

	constructor()
	{
		this.fifo = [];
	}

	fill(newElement)
	{
		this.fifo.push(newElement);
	}

	drop()
	{
		if(this.isEmpty())return "Empty"
		this.fifo.shift();
	}

	peek()
	{	
		if(this.isEmpty())
			return "Fifo Empty";

		else
			return this.fifo[0];
	}

	isEmpty()
	{
		if(this.fifo.length == 0) return true;
		else
			return false;
	}

	printPos()
	{
		var string = "";


		for(var i = 0 ; i < this.fifo.length;i++)
		{
			string += this.fifo[i].position +","
		}
	
		return string;
	}

}



function setup() {
	createCanvas(1100, 1100);
	graph()

}



function findPath(circles,final,last)
{
	for(var i = 0 ; i < final.length; i++)
	{
		if(final[i].position == last)
		{
			var path = final[i].previous;
			path = final[i].position + "," + path;
			path = path.split(',');
		
		}
	}
				

	for(var i = 0; i < path.length;i++)
	{
		console.log(path[i]);
		for(var j = 0; j < circles.length;j++)
		{

			if(path[i] == circles[j][0])
			{
				fill('red');
				textSize(5);
				console.log(3-i,circles[j][1]*10+500,circles[j][2]*10+500);
				text(3-i,circles[j][1]*10+500,circles[j][2]*10+500);
			}
		}
	}
}

function graph(){


var n = 3;
circles =[
["A1",0, 0, 1],
["A2",4 ,0 ,4],
["A3",1, 0 ,2],
//["A4",22, 1, 8],
//["A5",22 ,-8 ,8],
//["A6",30, 2, 6]
]
visualization();

graph = new Array();

for(var i = 0; i < n; i++)
{
		graph[i] = new Array;

	for(var j =0; j < n;j++)
	{
		if(i != j && isIntersect(circles[i],circles[j]))
		{
			graph[i].push(circles[j][0]);
		}
	}
	
}
console.log(n)
var last = "A" + n;

seen = [];

for(var i = 0 ;i < graph.length;i++)
{
	seen[i] = [];
	for(var j = 0;j < graph[i].length;j++)
	{
		seen[i].push(graph[i][j])
	}
}

for(var i = 0 ;i < graph.length;i++)
{
	for(var j = 0;j < graph[i].length;j++)
	{
		if (graph[i][j] == "A1")
			seen[i][j] = true; 
	}
}


final = [];

result = shortest_path(graph,seen,last,final);
console.log(result)
console.log(seen);
console.log(graph);
console.log(final);
findPath(circles,final,last);

if(result == -1)
	{
		var content = "Output: " + "No route to the destination";
		document.getElementById("output").innerHTML=content;
	}
	else
	{	



		var content = "Output: " + result;
		document.getElementById("output").innerHTML=content;
	}

}

function visualization(){
//Adds 50 besause (0,0) is top left corner
//Coordinate system center center of coordinate system is (50,50)

for(var i = 0 ; i < 100;i++)
	{
		for(var j = 0; j < 100;j++)
		{
			var x = i * 10;
			var y = j * 10;
			rect(x,y,10,10);
		}
	}

	stroke('red');
	fill('red');
	line(500,0,500,1000);
	line(0,500,1000,500);

//stroke('black');
//ellipse(0+500,0+500,10*3)

for(var i = 0 ; i < circles.length;i++)
{
stroke('black');
noFill();
console.log(circles[i][1]*10+500,circles[i][2]*10+500,(circles[i][3]*10)*2);
ellipse(circles[i][1]*10+500,circles[i][2]*10+500,(circles[i][3]*10)*2);

}

}


function isIntersect(circleA,circleB){

	var distanceA_B = sqrt((circleA[1] - circleB[1])**2 + (circleA[2] - circleB[2])**2)
	if (distanceA_B < (circleA[3] + circleB[3]) && distanceA_B > abs(circleA[3]-circleB[3]))
	{
	console.log("circleA = ",circleA[0],"circleB = ",circleB[0],"distanceA_B = ",distanceA_B,"check1 = ",circleA[3] + circleB[3],"check2 = ",abs(circleA[3]-circleB[3]))

		return true;
	}
	
	else
	{ 
		return false;
	}
}


function shortest_path(graph,seen,last,final)
{
	queue = new deque();
	start = new path("A1",0,"");

	queue.fill(start);


while(!queue.isEmpty())
{
	console.log(queue.isEmpty())

	current = queue.peek();
	queue.drop();

	if(current.position == last)
	{
		return current.distance;
	}

	var branch = current.position[current.position.length-1];
	branch = parseInt(branch) -1 ;

	for(var i = 0 ; i < graph[branch].length;i++)
	{
		
		if(seen[branch][i] != true)
		{	
			console.log(graph[branch][i]);
			point = new path(graph[branch][i],current.distance+1,current.position + "," + current.previous);
			final.push(point);
			queue.fill(point);
			seen[branch][i] = true;
		}
	}

}
return -1;

}

function draw(){
}