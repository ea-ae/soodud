const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');


module.exports = merge(common, {
    mode: 'production',
    output: {
        filename: '[name].[contenthash].bundle.js',
        publicPath: '/',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
            minSize: 15000, // 15kb
            // maxInitialRequests: Infinity,
            // minSize: 0,
            // cacheGroups: {
            //     vendor: {
            //         test: /[\\/]node_modules[\\/]/,
            //         name(module) {
            //             // get the name. E.g. node_modules/packageName/not/this/part.js
            //             // or node_modules/packageName
            //             const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];

            //             // npm package names are URL-safe, but some servers don't like @ symbols
            //             return `npm.${packageName.replace('@', '')}`;
            //         },
            //     },
            // },
        },
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
        }),
    ]
});
