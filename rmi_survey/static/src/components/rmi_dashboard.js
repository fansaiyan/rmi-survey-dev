/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
const { Component } = owl

export class RmiDashboard extends Component {
    setup(){

    }
}

RmiDashboard.template = "rmi_survey.RmiDashboard"
RmiDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("rmi_survey.rmi_dashboard", RmiDashboard)