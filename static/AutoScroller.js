/*
	自動捲動文字
	類似讀字機、歌詞等功能
*/

var Scroller = {
	Speed:1,
	Run: false,
	ScrollCtrl:null,
	NowVal:0,
	OnStop:function(){}
}

function move(ctrl){
	if (!Scroller.Run)
		return ;

	Scroller.NowVal += 1;
	//$("#val").text(Scroller.NowVal);
	if (Scroller.NowVal > Scroller.ScrollCtrl.height()){
		Scroller.Run = false;
		Scroller.OnStop();
	}
	ctrl.css('margin-top',-Scroller.NowVal);
	setTimeout(function(){
		move(ctrl,Scroller.NowVal);
	},Scroller.Speed);
}

//初始
Scroller.AutoScroll = function(ctrl){
	var ctrl_ = $("#" + ctrl);
	Scroller.ScrollCtrl = ctrl_.children(":first");
	//Scroller.Scroller = $("#scrollContent");
	//Scroller.ScrollCtrl.css('position', 'absolute');
	Scroller.NowVal = 0;
}

//開始
Scroller.Start = function(){
	if (Scroller.Run)
		return false;

	if (Scroller.ScrollCtrl == null)
		return false;

	//alert(Scroller.ScrollCtrl.height());
	//alert(Scroller.Speed);
	Scroller.Run = true;
	move(Scroller.ScrollCtrl);
	return true;
}

Scroller.Pause = function(){
	Scroller.Run = Scroller.Start()
}

Scroller.Reset = function(){
	Scroller.Run = false;
	Scroller.ScrollCtrl.css('margin-top',0);
	Scroller.NowVal = 0;
}