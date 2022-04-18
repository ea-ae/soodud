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
        port: 8002,
        hot: true,
        magicHtml: true,
        static: { directory: path.join(__dirname, 'public') },
        client: { progress: true },
        compress: true,
        watchFiles: {paths: ['./src/**/*']},
        historyApiFallback: {
            index: '/',
        },
        proxy: {
            '/api/v1': {
                target: {
                    host: '127.0.0.1',
                    protocol: 'http:',
                    port: 8001
                }
            }
        }
    },
});
