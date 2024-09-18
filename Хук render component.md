Данный хук нужен для прокидывания компонентов их плагинов и их отрисовки на шапке графика на дашборде. Представляет собой колбэк

Данный хук инициализируется в файле Chart.jsx (BI\superset-frontend\src\dashboard\components\gridComponents\Chart.jsx)

Далее хук прокидывается в нижний компонент Chart.jsx через connect в компоненте ChartContainer.jsx
![[Pasted image 20240815103709.png]]

В файле Chart.jsx хук хранится в пропсах
Далее хук прокидывается в дочерний компонент ChartRenderer. В данном компоненте хук помещается в объект hooks
![[Pasted image 20240815103858.png]]
Далее хук внутри объекта hooks передается в дочерний компонент SuperChart

Внутри компонента SuperChart хук внутри chartProps передается в компонент SuperChartCore. Далее в этом компоненте пропсы прокидываются в элемент Renderer.

Далее хук попадает в transformProps, затем прокидывается в EchartTimeSeries.tsx
В компоненте EchartTimeSeries.tsx определяются компоненты для рендеринга (rollingTypeButton, timeGrainSelect, stackValueSelect), которые передаются в хук renderComponent, где их значения присваиваются состоянию renderComponents:
![[Pasted image 20240815105256.png]]
![[Pasted image 20240815105246.png]]

Далее это состояние передается в компонент SliceHeader, где происходит отрисовка элементов из этого состояния