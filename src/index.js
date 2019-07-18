import React from 'react';
import ReactDOM from 'react-dom';
import BrowsingPage from './client/browsingPage';

ReactDOM.render(
  <BrowsingPage/>,
  document.getElementById('app')
);

module.hot.accept();