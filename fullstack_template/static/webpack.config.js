const webpack = require('webpack');const config = {
    entry:  __dirname + '/js/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
};module.exports = config;
//https://codeburst.io/creating-a-full-stack-web-application-with-python-npm-webpack-and-react-8925800503d9