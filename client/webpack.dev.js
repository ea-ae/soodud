const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');


module.exports = merge(common, {
    mode: 'development',
    devtool: 'eval',
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'devdist'),
        publicPath: '/',
        clean: true,
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',
        }),
    ],
    devServer: {
        port: 8080,
        hot: true,
        magicHtml: true,
        static: { directory: path.join(__dirname, 'public') },
        client: { progress: true },
        compress: true,
        port: 8001,
        watchFiles: {paths: ['./src/**/*']},
        historyApiFallback: {
            index: '/',
        },
    },
});
