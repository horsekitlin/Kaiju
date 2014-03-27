$(document).ready(function(){
    $( ".play_content" ).append($(".player_1_data").html());    
    $(".player").on('click',function(){
        var num = $(this).attr('name');
        var player = $(".player_"+num+"_data")
        $( ".play_content" ).text('')
        $( ".play_content" ).append(player.html());    
    })
})
