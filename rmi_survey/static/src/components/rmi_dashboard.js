/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"

const { Component, useState, onWillStart } = owl

export class RmiDashboard extends Component {
    setup(){
        this.state = useState({
            surveyFilter: 0,
            selectedFilterSurvey: null,
        })
        this.orm = useService("orm")

        onWillStart(async ()=> {
            await this.getFilteredSurvey()
        })
    }

    async getFilteredSurvey(){
        // let domain = [['active', '!=', ['false']]];
        const data = await this.orm.readGroup('survey.survey', [], ["id"], ["title"]);
        console.log('data ->', data)
        let filteredData = data.map(item => {
            const value = item.title;
            const totalAmount = item.service_total;
        });
        console.log(filteredData)
        this.state.selectedFilterSurvey = filteredData
    }
}

RmiDashboard.template = "rmi_survey.RmiDashboard"
RmiDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("rmi_survey.rmi_dashboard", RmiDashboard)