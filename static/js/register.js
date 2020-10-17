let vm = new Vue({
    el: "#app",
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: {
        // v-model
        username: "",
        password: '',
        password2: '',
        mobile: '',
        allow: false,
        image_code_url: '',
        image_code: '',
        uuid: '',
        sms_code_tip: '获取短信验证码',
        sms_code: '',
        // v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,
        send_flag: false,
        // error_message
        error_name_message: '',
        error_mobile_message: '',
        error_image_code_message: '',
        error_sms_code_message: ''
    },
    methods: {
        check_username: function () {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                // 匹配成功，则不展示
                this.error_name = false;
            } else {
                // 匹配失败，则进行展示
                this.error_name = true;
                this.error_name_message = '请输入5-20个字符的用户名'
            }
            if (this.error_name === false) {
                url = '/users/usernames/' + this.username + '/count/'
                axios.get(url, {
                    responseType: 'json'
                })
                    // 请求成功处理
                    .then(response => {
                        if (response.data.count === 1) {
                            // 用户名已经存在
                            this.error_name = true;
                            this.error_name_message = '用户名已经存在'
                        } else {
                            this.error_name = false
                        }
                    })
                    // 请求失败处理
                    .catch(error => {
                        console.log(error.response)
                    })
            }
        },
        check_password() {
            let re = /^[a-zA-Z0-9]{8,20}$/;
            this.error_password = !re.test(this.password);
        },
        check_password2() {
            this.error_password2 = this.password !== this.password2;
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
                this.error_mobile_message = '请输入正确的手机号'
            }
            if (this.error_mobile === false) {
                url = '/users/mobiles/' + this.mobile + '/count/'
                axios.get(url, {
                    responseType: 'json'
                })
                    // 请求成功处理
                    .then(response => {
                        if (response.data.count === 1) {
                            // 手机号已经存在
                            this.error_mobile = true;
                            this.error_mobile_message = '手机号已经存在'
                        } else {
                            this.error_mobile = false
                        }
                    })
                    // 请求失败处理
                    .catch(error => {
                        console.log(error.response)
                    })
            }
        },
        check_allow() {
            this.error_allow = !this.allow;
        },
        on_submit() {
            this.check_username()
            this.check_password()
            this.check_password2()
            this.send_sms_code()
            if (this.error_name || this.error_password || this.error_password2 || this.error_mobile || this.error_allow || this.error_image_code || this.error_sms_code) {
                // 禁止表单提交
                window.event.returnValue = false;
            }
        },
        generate_image_code() {
            this.uuid = generateUUID()
            this.image_code_url = '/image_codes/' + this.uuid + '/'
        },
        check_image_code() {
            if (this.image_code.length !== 4) {
                this.error_image_code_message = '请输入4位图形验证码';
                this.error_image_code = true
            } else {
                this.error_image_code = false
            }
        },
        check_sms_code() {
            if (this.sms_code.length !== 6) {
                this.error_sms_code_message = '请输入6位短信验证码';
                this.error_sms_code = true
            } else {
                this.error_sms_code = false
            }
        },
        send_sms_code() {
            if (this.send_flag === true){
                return
            }
            this.send_flag = true;
            // 校验手机号和图形验证码
            this.check_mobile();
            this.check_image_code();
            if (this.error_mobile === true || this.error_image_code === true) {
                return;
            }
            let url = 'sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    let sec = 60
                    if (response.data.code === '0') {
                        //定时器
                        let t = setInterval(() => {
                            if (sec === 1) {
                                // 定时器停止
                                clearInterval(t)
                                this.sms_code_tip = '获取短信验证码'
                                // 重新生成图形验证码
                                this.generate_image_code()
                                this.send_flag = false
                            } else {
                                sec -= 1
                                this.sms_code_tip = sec + '秒'
                            }
                        }, 1000)
                    }
                    else{
                        if(response.data.code === '4001'){
                            // 图形验证码有误
                            this.error_image_code_message = response.data.errmsg
                            this.error_image_code = true
                            this.send_flag = false
                        }
                    }
                })
                .catch(error => {
                    console.log(error.response)
                    this.send_flag = false
                })
        }
    },
    mounted() {
        this.generate_image_code()
    }
})