import React from 'react';
import { useEffect, useState } from 'react';
import ECharts from 'echarts-for-react';

import { QueryEvents, DetailedProduct, DetailedStoreProduct, DetailedPrice, Product } from './api';
import CloseButton from './buttons';


const ProductDetails = (props: {onClose: () => void, product: Product}) => { // mx-1.5 my-10 sm:m-6 md:m-12 lg:m-20 xl:m-32
    const [error, setError] = useState<{message: string} | null>(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [data, setData] = useState<DetailedProduct | null>(null);

    const fetchProductDetails = (events: QueryEvents, productId: number) => {
        const url = `${location.protocol}//${location.hostname}/api/v1/products/${productId}/`;
        fetch(url, {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(events.onSuccess, events.onError)
    }

    const getProduct = (productId: number) => fetchProductDetails(
        {
            onSuccess: res => { setData(res); setError(null); setIsLoaded(true); },
            onError: err => { setData(null); setError(err); setIsLoaded(true); }
        },
        productId
    );

    useEffect(() => {
        getProduct(props.product.id);
    }, [props.product]);

    let details = <></>;
    if (isLoaded && !error) {
        let title = '';
        let names: JSX.Element[] = [];
        data!.store_products.map(sp => {
            if (sp.name == props.product.name) {
                title = `${props.product.name} (${sp.store_name})`;
            } else {
                const name = `${sp.name} (${sp.store_name})`;

                names.push(
                    <p key={name} className="text-neutral-600 text-center text-xs md:text-sm leading-4">{name}</p>
                );
            }
        });

        details = (
            <>
            <p className="flex-grow mt-2 text-center font-semibold">{title}</p>
            {names}
            <PriceHistoryChart products={data!.store_products} />
            </>
        );
    } else {
        details = (
            <>
            <p className="flex-grow mt-2 text-center font-semibold">{props.product.name}</p>
            <p>Laeme...</p>
            </>
        );
    }

    return (
        <div className="shadow-xl border w-[90vw] md:w-[80vw] xl:w-[60vw] bg-stone-50 font-main text-neutral-800">
            <CloseButton onClose={props.onClose} />
            <div className="flex flex-col justify-center items-center p-1.5 sm:p-5 pt-10 text-sm sm:text-base">
                {details}
            </div>
        </div>
    );
}

const PriceHistoryChart = (props: {products: DetailedStoreProduct[]}) => {
    const getPriceDate = (startTime: string) => {
        let date = new Date(startTime);
        date.setHours(0, 0, 0, 0);
        return +date;
    }

    let dates: number[] = [];
    props.products.forEach(product => { // create x axis of dates
        product.prices.forEach(price => {
            dates.push(getPriceDate(price.start));
        });
    });

    dates = [...Array.from(new Set(dates))]; // remove duplicate dates and sort
    dates.sort();

    let dateAxis = dates.map(dateNumber => {
        let date = new Date(dateNumber);
        let day = date.getDate().toString().padStart(2, '0');
        let month = (date.getMonth() + 1).toString().padStart(2, '0');
        let year = date.getFullYear(); // % 100 => 2022 -> 22
        return [day, month, year].join('/');
    });

    let storePrices = props.products.map(product => {
        let priceHistory: (number | null)[] = new Array(dates.length);
        let priceIndex = 0;
        let lastPrice = null;

        for (let dateIndex = 0; dateIndex < dates.length; dateIndex++) {
            let outOfPrices = priceIndex >= product.prices.length;
            if (!outOfPrices && getPriceDate(product.prices[priceIndex].start) == dates[dateIndex]) {
                let price = product.prices[priceIndex].price;
                // priceHistory.push(price);
                priceHistory[dateIndex] = price;
                lastPrice = price;
                priceIndex++; // price has been assigned, move onto next one
                dateIndex--; // if next price is at the same date, overwrite
            } else {
                // priceHistory.push(lastPrice);
                priceHistory[dateIndex] = lastPrice;
            }
        }

        return {
            storeName: product.store_name,
            priceHistory: priceHistory,
            lastChecked: product.last_checked,
        };
    });

    let series = storePrices.map(storePrice => {
        let color;
        let zIndex;
        switch (storePrice.storeName) {
            case 'Coop':
                color = '#0070cc';
                zIndex = 5;
                break;
            case 'Prisma':
                color = '#088c44';
                zIndex = 4;
                break;
            case 'Rimi':
                color = '#d72323';
                zIndex = 3;
                break;
            case 'Selver':
                color = '#e8ce07';
                zIndex = 2;
                break;
            default:
                throw 'Unknown store name!';
        }

        return {
            name: storePrice.storeName,
            data: storePrice.priceHistory,
            type: 'line',
            z: zIndex,
            lineStyle: {color: color},
            itemStyle: {color: color},
            // smooth: true,
            // step: true,
            symbol: 'emptyCircle', // none
            animationDuration: 600,
            sampling: 'lttb',
        }
    });

    let options = {
        grid: { top: 8, right: 8, bottom: 70, left: 40 },
        toolbox: { feature: { restore: {} } },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            data: dateAxis,
        },
        yAxis: {
            type: 'value',
            scale: true,
            boundaryGap: [0, '100%'],
            axisLabel: { formatter: '{value}€' }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100,
            },
            {
                start: 0,
                end: 100,
            },
        ],
        tooltip: {
            trigger: 'axis',
        },
        series: series
    };

    return <ECharts option={options} style={{width: '100%'}} />
}

export default ProductDetails;
