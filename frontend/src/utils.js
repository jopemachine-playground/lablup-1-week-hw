const parseCookie = str => {
  if (str.trim() === "") return {};

  return str
  .split(';')
  .map(v => v.split('='))
  .reduce((acc, v) => {
    acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
    return acc;
  }, {});
}

export {
  parseCookie
}
