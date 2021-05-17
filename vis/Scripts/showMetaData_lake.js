function showMetaDataInfo(seg_id){
    sidebar.open('home');
    
    $('#segment_info').html('Segment ID: ' + seg_id );
    var meta_data_str = "";

    $('#historyHeatMap').html('');

    d3.json("Data/MetaData_Lake/" + seg_id + ".json").then(function(d) {
        var data = d.data;

        meta_data_str += "<div>Variable : IRFLakeVolume in m3</div>";
        if (data.Lake_name != "")
            meta_data_str += "<div>Lake Name : "+ data.Lake_name +"</div>";
        meta_data_str += "<div>Lake Area : "+ data.Lake_area +"</div>";

        $('#meta_info_div').html(meta_data_str);
    });
    drawHistoryHeatMapChart(seg_id, "IRFlakeVol");
}