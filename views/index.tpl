<!DOCTYPE html>
<html>

<head>
  <!-- Standard Meta -->
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

  <!-- Site Properties -->
  <title>{{title}}</title>

  <link rel="stylesheet" href="/css/jquery-ui.min.css" />
  <link rel="stylesheet" href="/css/jquery-ui.structure.min.css" />
  <link rel="stylesheet" href="/css/jquery-ui.theme.min.css" />
  <link rel="stylesheet" href="/semantic/semantic.min.css" />
  <link rel="stylesheet" href="/css/main.css" />

  <script src="/js/jquery-3.4.1.min.js"></script>
  <script src="/js/jquery-ui.min.js"></script>
  <script src="/js/jquery.serialize-object.min.js"></script>
  <script src="/semantic/semantic.min.js"></script>
  <script src="/js/plotly-latest.min.js"></script>

</head>

<body>
  <div class="ui fixed menu">
    <div class="ui container">
      <a href="#" class="header item">
        <!-- <img class="logo" src="assets/images/logo.png"> -->
        {{title}}
      </a>
    </div>
  </div>

  <div class="ui main text container">
    <div class="ui container">
      <form id="dataInput" class="ui form segment">
        <div class="two fields">
          <div class="field">
            <label>Data</label>
            <input id="file" type="file" accept=".csv, .xls, .xlsx, application/vnd.ms-excel" name="file">
          </div>
          <div class="field">
            <label>H</label>
            <input name="H" type="number" min="1" step="1" placeholder="4">
          </div>
        </div>
        <div class="two fields">
          <div class="field">
            <label>C</label>
            <input name="C" type="text" placeholder="[[0,0,0,1],[0,-1,0,1]]">
          </div>
          <div class="field">
            <label>Y</label>
            <input name="Y" type="text" placeholder="[1.2,0.1]">
          </div>
        </div>
        <div class="ui primary submit button">Submit</div>
        <div class="ui clear button">Clear</div>
      </form>
    </div>
  </div>
  <div class="ui main container">
    <div id="loaderSpin" class="ui active centered inline loader" style="display:none;">
    </div>
    <div id="output" class="ui container">
      <div class="ui column">
        <div id="chart" style="width: 100%;
            height: 500px;"></div>
      </div>
    </div>
  </div>

  <script src="/js/functions.js"></script>
  <script src="/js/main.js"></script>
</body>

</html>