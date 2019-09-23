firstQuadrant = [];
secondQuadrant = [];
thirdQuadrant = [];
fourthQuadrant = [];
seconds = [];
hours = [];
var i = 0;
var m = 0;
var k = 0;
var line = 0;
var globalX;
var globalY;
var check = true;



function setup() {
	createCanvas(1100, 1100);
	system();
	frameRate(1);
}

function draw() {
		if(i < seconds.length)
		{
			clear();
			system();


			stroke('black');
			rendar(seconds[i][0],seconds[i][1]);
			i +=1;	
		}
		else
		{
			i = 0;
		}
		console.log(i,m);
		if(m < seconds.length && i == 60) 
		{
			stroke('blue');
			line(globalX,globalY,seconds[m][0],seconds[m][1]);
			if(m == 0 && check == false)
				m = 0;
			
			else
				m+=1;
			stroke('black');

			
		}

		else if(m > 0 && m < seconds.length)
		{
			stroke('blue');
			line(globalX,globalY,seconds[m][0],seconds[m][1])
			stroke('black');
		}

		else if(m == 0 && seconds.length != 0 && check == true)
		{	
			if(k == 60)check = false;
			stroke('blue');
			line(globalX,globalY,seconds[seconds.length-1][0],seconds[seconds.length-1][1])
			stroke('black');
			k++;	
		}

		else
		{
			m = 0;
		}
	
}

function rendar(x,y)
{	for(var i = 0; i < seconds.length;i++)
	{
		stroke('green');
		fill('red');
		ellipse(seconds[i][0],seconds[i][1],2)
		noFill();
	}
	stroke('yellow');
	line(globalX,globalY,x,y);
	stroke('black');
}


function system(){
	noFill();
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
}


function calc(){
	var xCoord = document.getElementById('xcoord').value;
	var yCoord = document.getElementById('ycoord').value;
	var radius = document.getElementById('radius').value;
	var points = document.getElementById('points').value;

	xCoord = xCoord*10;
	xCoord = 500 + xCoord;

	yCoord = yCoord*10;
	console.log(yCoord);
	if(yCoord >= 0)
	{
		yCoord = 500 - yCoord;
	}
	else
	{
		yCoord = 500 - yCoord;
	}

	radius = radius*10;

	console.log(xCoord,yCoord,radius,points);
	globalX = xCoord;
	globalY = yCoord;
//Center (500,500)
	var degreePerTick = parseInt(360) / points;
	console.log(degreePerTick);
	var degree = 0;
	


	while(degree <= 90)
	{
		var y = Math.sin(degree * (Math.PI/ 180))* radius;
		var x = sqrt((radius**2) - (y**2));
		//ellipse(x+xCoord,y+yCoord,1);


		//First Quadrant
		stroke('green');
		ellipse(xCoord + x,yCoord - y,2);
		firstQuadrant.push([xCoord + x,yCoord - y]);
		
		//Second Quadrant
		stroke('green');
		ellipse(xCoord - x,yCoord - y,2);
		secondQuadrant.push([xCoord - x,yCoord - y]);

		//Third Quadrant
		stroke('green');
		ellipse(xCoord - x,yCoord+y,2);
		thirdQuadrant.push([xCoord - x,yCoord + y]);

		//Fourth Quadrant
		stroke('green');
		ellipse(xCoord+x,yCoord + y,2);
		fourthQuadrant.push([xCoord + x,yCoord + y]);

		degree = degree + degreePerTick;
		stroke('black');

	}
	firstQuadrant = firstQuadrant.reverse();
	thirdQuadrant = thirdQuadrant.reverse();

	helper = [];
	helper = helper.concat(firstQuadrant);
	helper.splice(helper.length-1,1);
	helper = helper.concat(fourthQuadrant);
	helper.splice(helper.length-1,1);
	helper = helper.concat(thirdQuadrant);
	helper.splice(helper.length-1,1);
	helper = helper.concat(secondQuadrant);
	helper.splice(helper.length-1,1);

	for(var i = 0; i < helper.length;i++)
	{
		if(i % 5 == 0)
			hours.push(helper[i]);

	}
	console.log(hours);



	firstQuadrant.splice(0,1);
	fourthQuadrant.splice(0,1);
	thirdQuadrant.splice(0,1);
	secondQuadrant.splice(0,1);


	seconds = seconds.concat(firstQuadrant);
	seconds = seconds.concat(fourthQuadrant);
	seconds = seconds.concat(thirdQuadrant);
	seconds = seconds.concat(secondQuadrant);

	console.log(firstQuadrant,secondQuadrant,thirdQuadrant,fourthQuadrant);
	console.log(seconds);


}


