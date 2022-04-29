import React, { ChangeEventHandler, useState } from 'react';
import { Search } from 'react-router';


const SearchBar = (props: {onSearch: (searchQuery: string) => void}) => {
    let [searchText, setSearchText] = useState<string>('');

    const search = () => props.onSearch(searchText);

    return (
        <form onSubmit={e => { e.preventDefault(); search(); }}
              className="flex sm:col-start-2 md:col-start-3 xl:col-start-1 row-start-2
                         col-span-10 sm:col-span-8 md:col-span-6 xl:col-span-3 shadow xl:sticky top-3">
            <SearchInput text={searchText} onChange={e => setSearchText(e.target.value)} />
            <SearchButton onClick={search} />
        </form>
    );
}

type SearchInputProps = {
    text: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    // onEnter: (e: React.KeyboardEvent) => void;
}

const SearchInput = (props: SearchInputProps) => {
    return (
        <input type="text" autoComplete="off" name="search" tabIndex={1}
               onChange={props.onChange} value={props.text} placeholder="Otsi tooteid..."
               className="flex-grow appearance-none h-12 px-4 py-2 focus:outline-none border-0
                          bg-stone-50 text-base text-stone-800" />
    );
}

const SearchButton = (props: {onClick: () => void}) => {
    return (
        <div onClick={props.onClick} className="flex flex-col h-12 w-12 justify-center bg-blue-500">
            <span className="material-icons select-none cursor-pointer text-center text-neutral-100 text-3xl">
                search
            </span>
        </div>
    );
}

export default SearchBar;
