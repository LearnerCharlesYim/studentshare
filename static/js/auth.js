
// 点击登录按钮，弹出模态对话框
$(function () {
    $(".login-btn").click(function () {
        $('.scroll-wrapper').css({'left':0});
        $(".mask-wrapper").show();
    });

    $(".close-btn").click(function () {
        $('.signin-group').find('input[name="username"]').val('');
        $('.signin-group').find('input[name="password"]').val('');
        $(".mask-wrapper").hide();
    });
});

$(function () {
    $(".signin-btn").click(function () {
        $('.scroll-wrapper').css({'left':-400});
        $(".mask-wrapper").show();
    });
    $(".close-btn").click(function () {
        $('.signup-group').find('input[name="username"]').val('');
        $('.signup-group').find('input[name="password1"]').val('');
        $('.signup-group').find('input[name="password2"]').val('');
        $(".mask-wrapper").hide();
    });
});


$(function () {
    $(".switch").click(function () {
        var scrollWrapper = $(".scroll-wrapper");
        var currentLeft = scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);
        if(currentLeft < 0){
            scrollWrapper.animate({"left":'0'});
        }else{
            scrollWrapper.animate({"left":"-400px"});
        }
    });
});

$(function () {
    layui.use('layer',function () {
        var layer = layui.layer;

        $('.signup-group').find('.submit-btn').click(function () {

            var username = $('.signup-group').find('input[name="username"]').val();
            var password1 = $('.signup-group').find('input[name="password1"]').val();
            var password2 = $('.signup-group').find('input[name="password2"]').val();
            if(username === '' ){
                layer.msg('请输入用户名');
                return
            }
            if(password1 === '' || password2 === '' ){
                layer.msg('请输入密码');
                return;
            }
            if(password1 !== password2){
                layer.msg('两次密码不一致');
                return;
            }

            $.ajax({
                url:'signup/',
                type:'POST',
                data:{
                    'username':username,
                    'password':password1
                },
                success:function (data) {
                    if(data['code'] === 200){
                        $(".mask-wrapper").hide();
                        layer.msg('注册成功', {icon: 1});

                    }else{
                       layer.msg(data['message'],{icon:2});
                    }
                },

            })
        })

        $('.signin-group').find('.submit-btn').click(function () {

            var username = $('.signin-group').find('input[name="username"]').val();
            var password = $('.signin-group').find('input[name="password"]').val();
            var remember = $('.signin-group').find('input[name="remember"]').val();

            if(username === '' ){
                layer.msg('请输入用户名');
                return
            }


            $.ajax({
                url:'login/',
                type:'POST',
                data:{
                    'username':username,
                    'password':password,
                    'remember':remember?1:0
                },
                success:function (data) {
                    if(data['code'] === 200){
                        $(".mask-wrapper").hide();
                        layer.msg(data['message'], {icon: 1});

                    }else{
                       layer.msg(data['message'],{icon:2});
                    }
                },

            })
        })

    });
});