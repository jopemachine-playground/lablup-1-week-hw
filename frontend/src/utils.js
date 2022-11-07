const parseCookie = string_ => {
	if (string_.trim() === '') {
		return {};
	}

	return string_
		.split(';')
		.map(v => v.split('='))
		.reduce((acc, v) => {
			acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
			return acc;
		}, {});
};

export {
	parseCookie,
};
