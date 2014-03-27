$(function(){
		// 倒數時間為 1 分 30 秒, 格式為 mm分ss秒
		// 時間到了跳出對話方塊
		$('#counter2').countdown({
			image: 'img/digits.png',
			startTime: '01:30',
			timerEnd: function(){
				alert('時間終了!');
			},
			format: 'mm:ss'
        });
	});
