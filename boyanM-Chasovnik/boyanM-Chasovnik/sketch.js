seconds = [];
hours = [];

seenSeconds= [];
seenMinutes= [];
seenHours = [];

var sec = 0;
var minutes = 0;
var hour1 = 0;

var globalX;
var globalY;




function setup() {
	createCanvas(1100, 1100);
	system();

	frameRate(60);
}

function draw() {
	clear();
	system();

	if(seenSeconds[sec] != true && seenSeconds.length != 0 && sec < 60)
	{	
	console.log(sec);

		rendar(seconds[sec][0],seconds[sec][1]);
		seenSeconds[sec] = true;
		drawMins(sec);
		sec++;
	}

	else
	{
		drawMins(sec);
		if(seconds.length != 0)rendar(seconds[0][0],seconds[0][1]);
		for(var i = 0 ; i < seenSeconds.length;i++)
		{
			seenSeconds[i] = false;
		}
		sec = 0;

	}


console.log(minutes);



}


function drawHours(minutes)
{
		if(minutes == 60 && hour1 < 12 && seenHours[hour1] != true)
		{
			seenHours = true;
			stroke('pink');
			line(globalX,globalY,hours[hour1][0],hours[hour1][1])
			stroke('black');
		}

		else if(minutes == 60 && hours == 12 && seenHours[hour1] != true)
		{
			if(hours.length != 0)
			{
			stroke('pink');
			line(globalX,globalY,hours[0][0],hours[0][1]);
			stroke('black');
			}
			for(var i = 0 ; i < hours.length;i++)
			{
				hours[i] = false;
			}
		}

		else
		{
			console.log(hour1);
			if(hours.length != 0)
			{
			stroke('pink');
			line(globalX,globalY,hours[hour1][0],hours[hour1][1]);
			stroke('black');
			}
		}
}


function drawMins(sec)
{
	if(sec == 60 && minutes < 60 && seenMinutes[minutes] != true)
	{	
		
		seenMinutes[minutes] = true;
		if(seconds.length != 0)
		{
			drawHours(minutes);
			stroke('blue');			
			line(globalX,globalY,seconds[minutes][0],seconds[minutes][1]);
			stroke('black');
			minutes++;

		}
	}
	
	else if(sec == 60 && minutes == 60 && seenMinutes[minutes] != true)
	{
		if(seconds.length != 0)
		{
			drawHours(minutes);
			stroke('blue');
			line(globalX,globalY,seconds[minutes][0],seconds[minutes][1]);
			stroke('black');
		}
		for(var i = 0 ; i < seenSeconds.length;i++)
		{
			seenSeconds[i] = false;
		}
		minutes = 0;

	}

	else
	{
		if(seconds.length != 0)
		{	
			drawHours(minutes);
			stroke('blue');
			line(globalX,globalY,seconds[minutes][0],seconds[minutes][1]);
			stroke('black');
		}
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
	noFill();
	stroke('black')
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
	

	help = [];
	while(degree <= 360)
	{
		var y = Math.sin(degree * (Math.PI/180))* radius;
		var x = sqrt((radius**2) - (y**2));
		//ellipse(x+xCoord,y+yCoord,1);

		if(degree >= 0 && degree <= 90)
		{
			x = xCoord + x;
			y = yCoord + y;
			if(degree != 0)
			{
			seconds.push([x,y]);
			}
		}

		if(degree > 90 && degree <= 180)
		{
			x = xCoord - x;
			y = yCoord + y;
			seconds.push([x,y]);
		}
		
		if(degree > 180 && degree <= 270)
		{
			x = xCoord - x;
			y = yCoord + y;
			seconds.push([x,y]);
		}
		
		if(degree > 270 && degree <= 360)
		{
			x = xCoord + x;
			y = yCoord + y;
			help.push([x,y]);
		}

		console.log(x,y);
		stroke('green');
		ellipse(x,y,2);

		degree = degree + degreePerTick;
		stroke('black');
	}

	for(var i = help.length - 1 ; i >= 0;i--)
	{
		seconds.unshift(help[i]);
	}

	var lastElement = seconds.splice(seconds.length-1,1);
	seconds.unshift(lastElement[0]);
	console.log(seconds);

	for(var i = 0; i < seconds.length;i++)
	{
		seenSeconds.push(false);
		seenMinutes.push(false);
	}

	for(var i = 0;i < seconds.length;i++)
	{
		if(i % 5 == 0)
		{
			hours.push(seconds[i]);
			seenHours.push(false);
		}
	}	


}


