import React from 'react';
import { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';

import Banner from './banner';
import SearchBar from './search_bar';
import ProductList from './product_list';
import './index.css';

export interface QueryEvents {
    onSuccess: (result: any) => void;
    onError: (error: any) => void;
}

export interface ProductAPIQuery {
    offset: number;
    length: number;
    reverse: boolean;
    search?: string;
}

export interface ProductListJSON {
    results: ProductJSON[];
}

interface ProductJSON {
    id: number;
    name: string;
    store_products: StoreProduct[];
}

interface StoreProduct {
    store_name: string;
    last_checked: string;
    price: {
        start: string;
        base_price: number;
        price: number;
        type: string;
    }
}

export class Product {
    id: number;
    name: string;
    prices: Prices;

    constructor(json: ProductJSON) {
        this.id = json.id;
        this.name = json.name;
        this.prices = {};
        json.store_products.forEach(sp => {
            this.prices[sp.store_name.toLowerCase()] = {
                basePrice: sp.price.base_price,
                actualPrice: sp.price.price,
                discount: sp.price.type as Discount
            };
        });
    }
}

interface Prices {
    [key: string]: Price;
}

export interface Price {
    basePrice?: number;
    actualPrice: number;
    discount: Discount;
}

export enum Discount {
    None = 'NONE',
    Normal = 'NORMAL',
    Member = 'MEMBER'
}

const App = () => {
    const list_offset = 0; // set to 100 for demo
    const list_length = 100; // 100 max
    const reverse_order = true;

    const [error, setError] = useState<{message: string} | null>(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [items, setItems] = useState<ProductListJSON | []>([]);

    const fetchProducts = (events: QueryEvents, query: ProductAPIQuery) => {
        const base_url = `${location.protocol}//${location.hostname}:8001/api/v1/products/?`;
        let params = `limit=${query.length}&offset=${query.offset}&reverse=${query.reverse}`;
        if (query.search !== undefined) params += `&search=${query.search}`;

        fetch(base_url + params, {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(events.onSuccess, events.onError)
    }

    const sendProductQuery = (search?: string) => fetchProducts(
        {
            onSuccess: res => { setItems(res); console.log('s'); setIsLoaded(true); },
            onError: err => { setError(err); console.log('e'); setIsLoaded(true); }
        },
        {offset: list_offset, length: list_length, reverse: reverse_order, search: search}
    );

    const onSearch = (searchQuery: string) => {
        console.log(`sending ${searchQuery}`);
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

