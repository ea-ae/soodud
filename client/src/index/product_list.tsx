import React from 'react';

import { ProductListJSON, Product } from './api';
import ProductHeader from './product_header';
import ProductRow from './product_row';

export const ProductList = (props: {isLoaded: boolean, products: ProductListJSON | [], error?: string}) => {
    const stores = ['Coop', 'Prisma', 'Rimi', 'Selver'];
    const status_style = 'py-5 text-center tracking-wider text-base';
    const item_layout = 'inline-block min-w-[3.5em] sm:min-w-[5em] sm:w-[5em] mt-1 ml-1 md:mt-0 text-center';
    const isEmpty = ((props.products as ProductListJSON).results ?? [1]).length == 0;

    return (
        <div className="row-start-3 xl:row-start-auto xl:row-span-3 col-span-10 xl:col-span-7 bg-transparent text-stone-800">
            <div className="shadow-sm cursor-default pb-2 bg-stone-50 text-sm lg:text-base">
                <ProductHeader stores={stores} item_layout={item_layout} />
                {props.isLoaded ? (props.products as ProductListJSON).results?.map(p => {
                    let product = new Product(p);
                    return <ProductRow key={product.id} stores={stores} product={product} item_layout={item_layout} />;
                }) : <div className={`${status_style}`}>Laeme...</div>}
                {isEmpty && props.isLoaded ? <div className={`${status_style}`}>Tooteid ei leitud</div> : <></>}
                {props.error ? <div className={`${status_style}`}>Error! {props.error}</div> : <></>}
            </div>
        </div>
    );
}

export default ProductList;
