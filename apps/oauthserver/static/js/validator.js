/*
 * 
 */
function check_login() {
	var email = document.getElementsByName('email')[0].value;
	var password = document.getElementsByName('password')[0].value;
	var validator = [/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/, /.{6,10}/];
	if (!validator[0].test(email) || !validator[1].test(password)) {
		alert('用户名或密码格式不对');
		return false;
	}
	return true;
}

/*
 *
 */
function check_register() {
	var username = document.getElementsByName('username')[0].value;
	var email = document.getElementsByName('email')[0].value;
	var password = document.getElementsByName('password')[0].value;
	var validator = [/.{6,8}/, /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/, /.{6,10}/];
	console.log(validator[0].test(username));
	if (!validator[0].test(username) || !validator[1].test(email) || !validator[2].test(password)) {
		alert('register failed!');
		return false;
	}
	return true
}