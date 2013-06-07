/*
	計時器
*/

var cTimer = {
	OutputObj:null,
	Run:false,
	Powers:{
		// Yeah this is major overkill...
		'ms': 1,
		'cs': 10,
		'ds': 100,
		's': 1000,
		'das': 10000,
		'hs': 100000,
		'ks': 1000000
	},
	PassTime:0		//經過多少時間(依據Power來決定單位)

}

//往左補0
function paddingLeft(str,lenght){
	if(str.length >= lenght)
		return str;
	else
		return paddingLeft("0" +str,lenght);
}

function TimeRun(power){
	setTimeout(function(){
		if ( !cTimer.Run )
			return ;
		cTimer.PassTime += cTimer.Powers[power]; 
		$("#"+cTimer.OutputObj).text(cTimer.ParseTime(cTimer.PassTime));
		TimeRun(power);
	},cTimer.Powers[power]);
}

cTimer.ParseTime = function(passTime){
		var passSec_ = passTime / 1000;
		var min_ = Math.floor(passSec_ / 60);
		var modSec_ = passSec_ % 60;
		var hr_ = Math.floor(min_ / 60);
		var modMin_ = min_ % 60;
		var modHr_ = hr_ % 24;
		var final_ = paddingLeft(modHr_.toString(),2) + ":" + paddingLeft(modMin_.toString(),2) + ":" +
					paddingLeft(modSec_.toString(),2);

		//alert(min_+","+cTimer.PassTime+","+final_);
		return final_;
}

cTimer.Start = function(power){
	if (cTimer.Run)
		return false;

	if (cTimer.OutputObj == null)
		return false;

	cTimer.Run = true;
	//cTimer.PassTime = 0;
	TimeRun(power);
	return true;
}

cTimer.Pause = function(){
	cTimer.Run = cTimer.Start('s');
}

cTimer.Stop = function(){
	cTimer.Run = false;
	cTimer.PassTime = 0;
	$("#"+cTimer.OutputObj).text(cTimer.ParseTime(cTimer.PassTime));
}

cTimer.Reset = function(){
	cTimer.Run = false;
	$("#"+cTimer.OutputObj).text("00:00:00");
	cTimer.PassTime = 0;
}