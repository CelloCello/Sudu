/*
	自動捲動文字
	類似讀字機、歌詞等功能
*/

var Scroller = {
	Speed:10,
	Run: false,
	ScrollCtrl:null,
	NowVal:0
}

function move(ctrl){
	if (!Scroller.Run)
		return ;

	Scroller.NowVal += 1;
	$("#val").text(Scroller.NowVal);
	if (Scroller.NowVal > Scroller.ScrollCtrl.height()){
		Scroller.Run = false;
	}
	ctrl.css('margin-top',-Scroller.NowVal);
	setTimeout(function(){
		move(ctrl,Scroller.NowVal);
	},10);
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
		return ;

	if (Scroller.ScrollCtrl == null)
		return ;

	//alert(Scroller.ScrollCtrl.height());
	Scroller.Run = true;
	move(Scroller.ScrollCtrl);
}

Scroller.Pause = function(){
	Scroller.Run = !Scroller.Run;
	if (Scroller.Run)
		Scroller.Start();
}

Scroller.Reset = function(){
	Scroller.Run = false;
	Scroller.ScrollCtrl.css('margin-top',0);
	Scroller.NowVal = 0;
}