import React from 'react';
import ReactDOM from 'react-dom';

import Banner from './banner';
import SearchBar from './search_bar';
import ProductList from './product_list';
import './index.css';


const App = () => {
    return (
        <>
        <Banner />
        <SearchBar />
        <ProductList />
        </>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);

