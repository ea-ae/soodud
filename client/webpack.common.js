const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');


module.exports = {
    entry: {
        index: './src/index/index.tsx',
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: 'src/index/index.html',
            filename: 'index.html',
            chunks: ['index'],
            favicon: 'public/favicons/favicon.ico',
        }),
    ],
    module: { rules: [
        {
            test: /\.(js|jsx|ts|tsx)$/,
            use: [{
                loader: 'babel-loader',
                options: {
                    presets: [
                        '@babel/preset-env',
                        '@babel/preset-react',
                        '@babel/preset-typescript'
                    ],
                    plugins: [
                        '@babel/proposal-class-properties',
                        '@babel/proposal-object-rest-spread',
                    ]
                },
            },],
        },
        {
            test:/\.css$/,
            include: [
                path.resolve(__dirname, 'src'),
            ],
            use: [
                'style-loader',
                {
                    loader: MiniCssExtractPlugin.loader,
                    options: { esModule: false } // this fixes a weird bug
                },
                'css-loader',
                'postcss-loader'
            ],
        },
    ]},

};
