(function(){
    var jquery_version = '3.4.1';
    var site_url = 'https://127.0.0.1:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height = 100;

    function bookmarklet(msg){
        //加载css
        var css = $('<link>');
        css.attr({
            rel : 'stylesheet',
            type : 'text/css',
            href : static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        $('head').append(css);
        //加载html
        box_html = '<div id="bookmarklet">\
        <a href="#" id="close">&times;</a>\
        <h1>Select an image to bookmark:</h1>\
        <div class="images"></div></div>'
        $('body').append(box_html);

        //单击关闭按钮就移除bookmarklet div的事件
        $('#bookmarklet #close').click(function(){
            $('#bookmarklet').remove();
        })

        //寻找图片并展示
        $.each($('img[src$=jpg]'),function(index,image){
            if($(image).width()>=min_width && $(image).height()>=min_height){
                image_url = $(image).attr('src');
                $('#bookmarklet .images').append('<a href="#"><img src="'+image_url+'"/></a>');
            }
        });

        //当用户选择了一张图片，打开这张图片的详细信息填写页面
        $('#bookmarklet .images a').click(function(e){
            selected_image = $(this).children('img').attr('src');
            //隐藏小窗口
            $('#bookmarklet').hide();
            //打开新窗口，提交图片
            window.open(site_url+'images/create/?url='
                        + encodeURIComponent(selected_image)
                        + '&title='
                        + encodeURIComponent($('title').text()),
                        '_blank');
        })
    };

    //检查jquery加载没有
    if(typeof window.jQuery != 'undefined'){
        bookmarklet();
    }
    else{
        //检查冲突
        var conflict = typeof window.$ != 'undefined';
        // 使用谷歌提供的jQuery
        var script = document.createElement('script');
        script.src = '//ajax.googleapis.com/ajax/libs/jquery/'+jquery_version+'/jquery.min.js';
        //把这个script元素插入到head里
        document.head.appendChild(script);
        //创建一个方法，等待script加载
        var attempts = 15;
        (function(){
            //再检查一下jquery是不是undefined
            if(typeof window.jQuery == 'undefined'){
                if(--attempts>0){
                    //隔一小段时间调用一次自己
                    window.setTimeout(arguments.callee,250);
                }
                else{
                    //已经试了很多次，报错
                    alert('An error occurred while loading jQuery');
                }
            }
            else{
                bookmarklet();
            }
        })();

    }

})();