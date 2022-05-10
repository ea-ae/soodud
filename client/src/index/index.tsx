import React from 'react';
import { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';

import {QueryEvents, ProductListAPIQuery, ProductListJSON } from './api';
import Banner from './banner';
import SearchBar from './search_bar';
import ProductList from './product_list';
import './index.css';


declare var __PRODUCTION__: string;


const App = () => {
    const list_offset = 0; // set to 100 for demo
    const list_length = 100; // 100 max
    const reverse_order = true;

    const [error, setError] = useState<{message: string} | null>(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [items, setItems] = useState<ProductListJSON | []>([]);

    const fetchProducts = (events: QueryEvents, query: ProductListAPIQuery) => {
        const port = __PRODUCTION__ ? '' : ':8001';
        const base_url = `${location.protocol}//${location.hostname}${port}/api/v1/products/?search=`;
        let params = `limit=${query.length}&offset=${query.offset}&reverse=${query.reverse}`;
        if (query.search !== undefined) params += `&search=${query.search}`;

        fetch(base_url + params, {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(events.onSuccess, events.onError)
    }

    const sendProductQuery = (search?: string) => fetchProducts(
        {
            onSuccess: res => { setItems(res); setError(null); setIsLoaded(true); },
            onError: err => { setItems([]); setError(err); setIsLoaded(true); }
        },
        {offset: list_offset, length: list_length, reverse: reverse_order, search: search}
    );

    const onSearch = (searchQuery: string) => {
        setIsLoaded(false);
        sendProductQuery(searchQuery);
    };

    useEffect(sendProductQuery, []);

    return (
        <>
        <Banner />
        <SearchBar onSearch={onSearch} />
        <ProductList isLoaded={isLoaded} products={items} error={error?.message} />
        </>
    );
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);

